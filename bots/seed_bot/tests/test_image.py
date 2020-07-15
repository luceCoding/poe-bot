from utils.screen_capture.app import App
import utils.imaging.conversions as conv
import poe.screen.image_detector as imgd
import timeit
import cv2
from pprint import pprint
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Luce\AppData\Local\Tesseract-OCR\tesseract.exe'
import timeit
from utils.imaging import text_finder as txtf

# screen = App(title='Path of Exile')
# rgb_screen = screen.get_screen_as_rgb_img()
# bgr_screen = conv.rgb_to_bgr(rgb_screen)
# path = r'C:\Users\Luce\Documents\My Games\Path of Exile\Screenshots\screenshot-0005.png'
# img = cv2.imread(path)
#98, 16, 117
# res = imgd.ImageDetector.find_first_occurrence_of(img, (117, 16, 98))
# x, y = res[0], res[-1]
# first = x[0], y[0]
# last = x[-1], y[-1]

# img = Image.quantize(colors=256, method=None, kmeans=0, palette=None, dither=1)


# img = cv2.rectangle(img,first,last,(0,255,0),3)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# cv2.imshow('img', bgr_screen)
# cv2.waitKey(0)

# def wrapper(func, *args, **kwargs):
#      def wrapped():
#          return func(*args, **kwargs)
#      return wrapped
# func = wrapper(txtf.find_text_on_screen, img)
# print(timeit.timeit(func, number=1))

# def find_text_on_screen(bgr_screen):
#     lower = np.array([97, 15, 116])
#     upper = np.array([99, 17, 118]) # 98, 16, 117
#     mask = cv2.inRange(bgr_screen.copy(), lower, upper)
#     print(mask.shape)
#
#     cv2.imshow('txt', mask)
#     cv2.waitKey(0)
#
#     # bgr_img = cv2.cvtColor(hsv_masked, cv2.COLOR_HSV2BGR)
#     # gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
#
#     # gray_img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     # cv2.imshow('img', gray_img)
#     # cv2.waitKey(0)
#
#     cnts = cv2.findContours(gray_img, cv2.RETR_EXTERNAL,
#                             cv2.CHAIN_APPROX_SIMPLE)[0]
#     for c in cnts:
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.04 * peri, True)
#         if len(approx) == 4:
#             (x, y, w, h) = cv2.boundingRect(approx)
#             el = gray_img[y:y + h, x:x + w]
#             pil_im = Image.fromarray(el)
#             yield pytesseract.image_to_string(pil_im)

path = r'C:\Users\Luce\Documents\projects\poe-bot\bots\seed_bot\tests\test_images\screenshot-0002.png'
img = cv2.imread(path)

# t = timeit.Timer(stmt="txtf.find_text_on_screen(test.A, test.B)", setup="import test")

# for txt in txtf.find_text_on_screen(img):
#     print(txt)



# masked = conv.get_masked_bgr_img(img, [145, 255, 117], offsets=[0,0,0])
#
# # lower = np.array([110, 10, 95]) #98, 16, 117
# # upper = np.array([120, 20, 100])
# # shapeMask = cv2.inRange(img, lower, upper)
# bgr = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
# gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
#
# # cv2.imshow('img', gray)
# # cv2.waitKey(0)
#
# cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL,
#                         cv2.CHAIN_APPROX_SIMPLE)[0]
# text_found = list()
# for c in cnts:
#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, 0.04 * peri, True)
#     if len(approx) == 4:
#         (x, y, w, h) = cv2.boundingRect(approx)
#         # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=5)
#
#         el = gray[y:y + h, x:x + w]
#         pil_im = Image.fromarray(el)
#
#         # cv2.imshow("obj", el)
#         # cv2.waitKey(0)
#
#         # print(pytesseract.image_to_string(pil_im))
#         text_found.append(pytesseract.image_to_string(pil_im))
#
#
# print(text_found)
