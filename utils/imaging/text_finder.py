import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Luce\AppData\Local\Tesseract-OCR\tesseract.exe'

def find_text_locations(bgr_img):
    return pytesseract.image_to_boxes(bgr_img)

def find_text_data(bgr_img, output_type=Output.DICT):
    return pytesseract.image_to_data(bgr_img,
                                     output_type=output_type,
                                     config='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

def find_text_strings(bgr_img):
    return pytesseract.image_to_string(bgr_img)