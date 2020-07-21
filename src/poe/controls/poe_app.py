from src.lib.screen_capture.app import App
from src.utils.imaging import conversions as conv
from src.poe.controls.input_handler import InputHandler
from src.poe.common.mask_manager import MaskManager
from src.poe.controls.minimap_handler import MinimapHandler
from src.poe.controls.image_handler import ImageHandler
from singleton_decorator import singleton
import time


@singleton
class POEApp:

    def __init__(self):
        self._app = App(title='Path of Exile')
        self.inputs = InputHandler(self._app)
        self.imaging = ImageHandler(self)

        self.mask_mapping = MaskManager()  # TODO: decouple?

        self._rgb_screen = None
        self._bgr_screen = None
        self._rgb_minimap = None
        self._bgr_minimap = None

        self.screen_width, self.screen_height = self.rgb_screen.size
        self.screen_center_pt = (self.screen_width // 2, self.screen_height // 2)
        self._minimap_handler = MinimapHandler(self, movement_distance=400)

    # def update_screen(self):
    #     del self._rgb_screen
    #     del self._bgr_screen
    #     self._rgb_screen = self._app.get_screen_as_rgb_img()
    #     self._bgr_screen = conv.rgb_to_bgr(self.rgb_screen)

    @property
    def rgb_screen(self):
        del self._rgb_screen
        self._rgb_screen = self._app.get_screen_as_rgb_img()
        return self._rgb_screen

    @property
    def bgr_screen(self):
        del self._rgb_screen
        del self._bgr_screen
        self._rgb_screen = self._app.get_screen_as_rgb_img()
        self._bgr_screen = conv.rgb_to_bgr(self.rgb_screen)
        return self._bgr_screen

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
        # cropped = self._minimap_handler.crop_minimap(self.bgr_screen)
        result = conv.get_masked_bgr_img(self.bgr_minimap,
                                         self.mask_mapping[mask])
        return result

    @property
    def minimap_handler(self):
        return self._minimap_handler

    def click_on_image_once(self, bgr_img, mouse='left', threshold=.6, pressed=''):
        pt = self.imaging.get_center_point_of_image_in_screen(bgr_img, threshold)
        if pt:
            # self.inputs.move_mouse(coords=pt)
            self.inputs.click_on_coords(mouse=mouse, coords=pt, pressed=pressed, double=True)
            return True
        return False

    def click_on_image_and_wait_for(self,
                                    first_bgr_img,
                                    second_bgr_img,
                                    mouse='left',
                                    max_tries=5,
                                    delay=1,
                                    first_threshold=.6,
                                    second_threshold=.6,
                                    pressed=''):
        for _ in range(max_tries):
            self.click_on_image_once(first_bgr_img, mouse, first_threshold, pressed=pressed)
            time.sleep(delay)
            if self.imaging.get_center_point_of_image_in_screen(second_bgr_img,
                                                                threshold=second_threshold) is not None:
                return True
        return False
