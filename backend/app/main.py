from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from . import auth, models, database, dicom_handler

app = FastAPI()

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