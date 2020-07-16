from src.utils.screen_capture.app import App
from src.utils.imaging import conversions as conv
from src.poe.input.input_handler import InputHandler
from src.poe.common.mask_manager import MaskManager
from src.utils.imaging import img_finder as imgf
from src.utils.math import coordinates as coord
from src.poe.screen.minimap_handler import MinimapHandler


class POEApp:

    def __init__(self):
        self._app = App(title='Path of Exile')
        self.inputs = InputHandler(self._app)
        self.mask_mapping = MaskManager()

        self.rgb_screen = self._app.get_screen_as_rgb_img()
        self.bgr_screen = conv.rgb_to_bgr(self.rgb_screen)
        self._rgb_minimap = None
        self._bgr_minimap = None

        self.screen_width, self.screen_height = self.rgb_screen.size
        self.screen_center_pt = (self.screen_width // 2, self.screen_height // 2)
        self._minimap_handler = MinimapHandler(self, 400)

    def update_screen(self):
        del self.rgb_screen
        del self.bgr_screen
        self.rgb_screen = self._app.get_screen_as_rgb_img()
        self.bgr_screen = conv.rgb_to_bgr(self.rgb_screen)

    @property
    def rgb_minimap(self):
        del self._rgb_minimap
        self._rgb_minimap = self._minimap_handler.crop_minimap(self.rgb_screen)
        return self._rgb_minimap

    @property
    def bgr_minimap(self):
        del self._bgr_minimap
        self._bgr_minimap = self._minimap_handler.crop_minimap(self.bgr_screen)
        return self._bgr_minimap

    def get_masked_bgr_minimap(self, mask):
        return conv.get_masked_bgr_img(self._minimap_handler.crop_minimap(self.bgr_screen),
                                       self.mask_mapping[mask])

    @property
    def minimap_handler(self):
        return self._minimap_handler

    def try_click_on_image(self, bgr_img, threshold=.6):
        pt = self.get_center_point_of_image_in_screen(bgr_img, threshold)
        if pt:
            self.inputs.click_on_coords(coords=pt)
            return True
        return False

    def get_center_point_of_image_in_screen(self, bgr_img, threshold=.6):
        self.update_screen()
        box_pts = imgf.get_template_img_location(self.bgr_screen, bgr_img, threshold)
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