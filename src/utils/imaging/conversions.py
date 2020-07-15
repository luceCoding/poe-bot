import cv2
import numpy as np


def rgb_to_bgr(rgb_img):
    numpy_img = np.array(rgb_img)
    return cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)

def bgr_to_gray(bgr_img):
    return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

def get_masked_bgr_img(bgr_img, hsv_color, offsets=[10, 10, 40]):
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
    upper = np.array([hsv_color[0] + offsets[0], hsv_color[1] + offsets[1], hsv_color[2] + offsets[2]])
    lower = np.array([hsv_color[0] - offsets[0], hsv_color[1] - offsets[1], hsv_color[2] - offsets[2]])
    mask = cv2.inRange(hsv_img, lower, upper)
    del hsv_img
    return cv2.bitwise_and(bgr_img, bgr_img, mask=mask)

