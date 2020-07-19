import cv2
import numpy as np
from src.utils.imaging import conversions as conv
import logging


def get_template_img_location(source_bgr_img, template_bgr_img, threshold):
    logging.debug('Template matching.')
    # cv2.imshow('', template_bgr_img)
    # cv2.waitKey(0)
    w, h = template_bgr_img.shape[:-1]
    res = cv2.matchTemplate(source_bgr_img, template_bgr_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)[::-1] # Switch columns and rows
    del res
    if len(loc) == 2 and len(loc[0]) and len(loc[1]):
        pt = [loc[0][0], loc[1][0]]
        result = np.asarray([pt, (pt[0] + h, pt[1] + w)])
        del w
        del h
        return result
    return None


def nearest_nonzero_idx(bgr_img, target):
    img = conv.bgr_to_gray(bgr_img)
    nonzero = cv2.findNonZero(img)
    del img
    if nonzero is None:
        return None
    distances = np.sqrt((nonzero[:, :, 0] - target[0]) ** 2 + (nonzero[:, :, 1] - target[1]) ** 2)
    nearest_index = np.argmin(distances)
    result = nonzero[nearest_index][0]
    del nonzero
    return result


def does_img_exist(source_bgr_img, target_bgr_img, threshold=.6):
    res = cv2.matchTemplate(source_bgr_img, target_bgr_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    result = len(loc)
    del res
    del loc
    return result
