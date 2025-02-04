# python modules
import numpy as np
import cv2
import PIL
import skimage
import re
from rembg import remove
from PIL import Image
import easyocr


#load and remove background image
def remove_background(input_image):
    input_image = cv2.imread(input_image)
    output_image = remove(input_image)
    return output_image

# function to preprocess the image
def image_preprocess(image):
    #resizing image
    resized = cv2.resize(image, (0, 0), fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # filtering noise
    denoised = cv2.fastNlMeansDenoisingColored(resized, None, 10, 10, 7, 21)
    # color enhancement
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced = cv2.merge((l, a, b))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    # adjusting contrast or sharpening of objects
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])  
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    return sharpened

 

def extract_ocr_results(image):
    reader = easyocr.Reader(['en'])  
    results = reader.readtext(image) 

    ocr_results = []
    
    # Iterate through detected text and store it in a list
    for bbox, text, prob in results:
        ocr_results.append((text, prob))
    
    return ocr_results



def extract_id_info(ocr_results):
    extracted_info = {
        "Country": None,
        "Unique ID Number": None,
        "Full Name": None,
        "Date of Birth": None,
        "Sex": None
    }

    for text, confidence in ocr_results:
        # print(f"Detected text: {text} (Confidence: {confidence:.4f})")
        text = text.upper()

        # Identify country
        if "REPUBLIC OF KENYA" in text or "JAMHURI YA KENYA" in text:
            extracted_info["Country"] = "Kenya"

        # Unique ID number 
        if re.fullmatch(r"\d{8,9}", text):
            extracted_info["Unique ID Number"] = text

        # Full Name
        if "PULL NAMES" in text or "FULL NAME"  in text or "FULLNAMES" in text:
            name_index = ocr_results.index((text, confidence)) + 1
            if name_index < len(ocr_results):
                extracted_info["Full Name"] = ocr_results[name_index][0]

        # Date of Birth
        if "DATE OF BIRTH" in text:
            dob_index = ocr_results.index((text, confidence)) + 1
            if dob_index < len(ocr_results):
                extracted_info["Date of Birth"] = ocr_results[dob_index][0]

        # Sex
        if text == "SEX":
            sex_index = ocr_results.index((text, confidence)) + 1
            if sex_index < len(ocr_results):
                extracted_info["Sex"] = ocr_results[sex_index][0]

    return extracted_info