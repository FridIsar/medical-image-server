import os
import pydicom

# Directory where DICOM files are stored
DATA_DIR = "data/"

# Function to retrieve patient name from DICOM file
def get_patient_name(dicom_filename: str) -> str:
    filepath = os.path.join(DATA_DIR, dicom_filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError("DICOM file not found.")
    try:
        ds = pydicom.dcmread(filepath)
        family_name = ds.PatientName.family_name
        given_name = ds.PatientName.given_name

        if family_name and given_name:
            return family_name + ", " + given_name
        else:
            return family_name or given_name
    except Exception as e:
        raise Exception("Error reading DICOM file")
