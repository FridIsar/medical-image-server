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
    
# Function to retrieve middle slice image from DICOM file
def get_middle_slice_image(dicom_filename: str) -> list:
    filepath = os.path.join(DATA_DIR, dicom_filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError("DICOM file not found.")
    
    try:
        ds = pydicom.dcmread(filepath)
        pixel_array = ds.pixel_array
        # TODO manipulating pixel data required GDCM on MacOS, check for Docker
        # Check if it's a 3D volume (multiple slices)
        if len(pixel_array.shape) == 3:
            # Extract the middle slice
            middle_index = pixel_array.shape[0] // 2
            middle_slice = pixel_array[middle_index]
        else:
            # If it's a single 2D image, return it as the "middle slice"
            middle_slice = pixel_array
        
        return middle_slice.tolist()  # Convert to a list of pixel values for JSON serialization
    except Exception as e:
        raise Exception("Error reading DICOM file: " + str(e))
