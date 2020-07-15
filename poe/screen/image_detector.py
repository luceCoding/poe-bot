import numpy as np
from utils.imaging import img_finder as imgf


class ImageDetector:

    @staticmethod
    def find_first_occurrence_of(img, pixel):
        indices = np.where(np.all(img == pixel))
        return indices

    @staticmethod
    def match_image_relative(source_bgr_img, template_bgr_img, pos, threshold=.6, area=200):
        x1, y1 = pos[0] + area, pos[1] + area
        x2, y2 = pos[0] - area, pos[1] + area
        cropped = template_bgr_img[y1:y2, x1:x2]
        return imgf.get_template_img_location(cropped, template_bgr_img, threshold)
