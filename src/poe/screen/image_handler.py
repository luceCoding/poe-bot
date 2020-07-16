from src.utils.imaging import img_finder as imgf
from src.utils.math import coordinates as coord
import time


class ImageHandler:

    def __init__(self, app):
        self.app = app

    def find_img_pt_in_screen(self, bgr_img, threshold=.6):
        self.app.update_screen()
        box_pts = imgf.get_template_img_location(self.app.bgr_screen, bgr_img, threshold)
        if box_pts is not None:
            center_img_pt = coord.get_centroid(box_pts)
            # cv2.rectangle(self.app.bgr_screen,
            #               (box_pts[1][0], box_pts[1][1]),
            #               (box_pts[0][0], box_pts[0][1]),
            #               color=(0, 0, 255),
            #               thickness=2)
            # cv2.imshow("img", self.app.bgr_screen)
            # cv2.waitKey(0)
            return (int(center_img_pt[0]), int(center_img_pt[1]))
        return None

    def wait_for_image_on_screen(self,
                                 image,
                                 retry_delay=1,
                                 post_delay=.25,
                                 max_tries=5,
                                 threshold=.6):
        n_tries = 0
        while not self.find_img_pt_in_screen(image, threshold=threshold):
            print("waiting:", n_tries)
            if n_tries >= max_tries:
                return False
            n_tries += 1
            time.sleep(retry_delay)
        time.sleep(post_delay)
        return True