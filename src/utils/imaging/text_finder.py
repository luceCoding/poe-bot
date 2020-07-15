import pytesseract
import cv2
from pytesseract import Output
from src.utils.imaging import conversions as conv
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Luce\AppData\Local\Tesseract-OCR\tesseract.exe'


def find_text_locations(bgr_img):
    return pytesseract.image_to_boxes(bgr_img)


def find_text_data(bgr_img, output_type=Output.DICT):
    return pytesseract.image_to_data(bgr_img,
                                     output_type=output_type,
                                     config='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')


def find_text_strings(bgr_img):
    return pytesseract.image_to_string(bgr_img)


def find_all_box_text_on_screen(bgr_screen):
    masked_bgr = conv.get_masked_bgr_img(bgr_screen,
                                         [145, 255, 117],
                                         offsets=[0, 0, 0])
    gray_img = cv2.cvtColor(masked_bgr, cv2.COLOR_BGR2GRAY)
    del masked_bgr
    # cv2.imshow("o", gray_img)
    # cv2.waitKey(0)
    cnts = cv2.findContours(gray_img, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[0]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            # cv2.rectangle(bgr_screen, (x, y), (x + w, y + h), (0, 255, 0), thickness=5)
            # cv2.imshow("o", bgr_screen)
            # cv2.waitKey(0)
            el = gray_img[y:y + h, x:x + w]
            pil_im = Image.fromarray(el)
            pt1 = (x, y)
            pt2 = (x + w, y + h)
            res = pytesseract.image_to_string(pil_im, output_type=Output.STRING), pt1, pt2
            del el
            del pil_im
            yield res


# def find_text_on_screen(bgr_screen, hsv_color, offsets=None):
#     masked_bgr = conv.get_masked_bgr_img(bgr_screen,
#                                          hsv_color,
#                                          offsets=[10, 10, 40])
#     gray_img = cv2.cvtColor(masked_bgr, cv2.COLOR_BGR2GRAY)
#     # cv2.imshow('gray', gray_img)
#     # cv2.waitKey(0)
#     text_data = find_text_data(gray_img)
#     return text_data
