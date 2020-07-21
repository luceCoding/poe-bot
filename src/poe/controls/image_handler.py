from src.utils.imaging import img_finder as imgf
from src.utils.math import coordinates as coord
from singleton_decorator import singleton
import time
import logging


@singleton
class ImageHandler:

    def __init__(self, app):
        self._app = app

    def wait_for_image_on_screen(self,
                                 bgr_img,
                                 retry_delay=.5,
                                 post_delay=.25,
                                 max_tries=10,
                                 threshold=.6):
        for _ in range(max_tries):
            logging.debug('Waiting for image: {}'.format(_))
            if self.get_center_point_of_image_in_screen(bgr_img,
                                                        threshold=threshold):
                return True
            time.sleep(retry_delay)
        time.sleep(post_delay)
        return False

    def get_center_point_of_image_in_screen(self, bgr_img, threshold=.6):
        # self._app.update_screen()
        box_pts = imgf.get_template_img_location(self._app.bgr_screen,
                                                 bgr_img,
                                                 threshold)
        if box_pts is not None:
            center_img_pt = coord.get_centroid(box_pts)
            # if debug:
            #     cv2.rectangle(self.app.bgr_screen,
            #                   (box_pts[1][0], box_pts[1][1]),
            #                   (box_pts[0][0], box_pts[0][1]),
            #                   color=(0, 0, 255),
            #                   thickness=2)
            #     cv2.imshow("img", self.app.bgr_screen)
            #     cv2.waitKey(0)
            return [int(center_img_pt[0]), int(center_img_pt[1])]
        return None