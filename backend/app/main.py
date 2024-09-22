from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os
from dotenv import load_dotenv
from . import auth, models, database, dicom_handler

load_dotenv()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")

app = FastAPI()

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
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
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