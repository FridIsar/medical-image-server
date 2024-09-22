from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from . import auth, models, database, dicom_handler
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database schema
    models.Base.metadata.create_all(bind=database.engine)
    
    # Startup event
    db = database.SessionLocal()
    username = "user"
    password = "password"
    
    # Check if the user already exists
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        # Create a new user
        hashed_password = auth.get_password_hash(password)
        new_user = models.User(username=username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        logging.info(f"Created default user: {username}")
    else:
        logging.info(f"User '{username}' already exists")
    db.close()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/up")
def read_root():
    return {"status": "ok"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/patient-name")
def get_patient_name(dicom_filename: str, token: str = Depends(auth.get_current_user)):
    try:
        # Retrieve the patient name from the DICOM file
        patient_name = dicom_handler.get_patient_name(dicom_filename)
        return {"patient_name": patient_name}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="DICOM file not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Error reading DICOM file")
    
@app.get("/middle-slice-image")
def get_middle_slice_image(dicom_filename: str, token: str = Depends(auth.get_current_user)):
    try:
        # Retrieve the middle slice image from the DICOM file
        image = dicom_handler.get_middle_slice_image(dicom_filename)
        return {"image": image}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="DICOM file not found")
    except Exception as e:
        logging.error(f"Error reading DICOM file: {e}")
        raise HTTPException(status_code=500, detail="Error reading DICOM file")