from utils.screen_capture.app import App
import utils.imaging.conversions as conv
from poe.input.inputhandler import InputHandler
from poe.screen.minimap import ScreenToMinimap
from poe.configs.masks import MaskManager


class POEApp:

    def __init__(self):
        self._app = App(title='Path of Exile')
        self.inputs = InputHandler(self._app)
        self.mask_mapping = MaskManager()

        self.rgb_screen = self._app.get_screen_as_rgb_img()
        self.bgr_screen = conv.rgb_to_bgr(self.rgb_screen)
        self._rgb_minimap = None
        self._bgr_minimap = None
        self._prev_rgb_screen = None
        self._prev_bgr_screen = None
        self._prev_rgb_minimap = None
        self._prev_bgr_minimap = None

        w, h = self.rgb_screen.size
        self.screen_center_pt = (w // 2, h // 2)
        self._minimap_cropper = ScreenToMinimap(w, h)

    def update_screen(self):
        self._prev_rgb_screen = self.rgb_screen
        self._prev_bgr_screen = self.bgr_screen
        self.rgb_screen = self._app.get_screen_as_rgb_img()
        self.bgr_screen = conv.rgb_to_bgr(self.rgb_screen)

    @property
    def rgb_minimap(self):
        self._prev_rgb_minimap = self._rgb_minimap
        self._rgb_minimap = self._minimap_cropper.crop_minimap(self.rgb_screen)
        return self._rgb_minimap

    @property
    def prev_rgb_minimap(self):
        return self._prev_rgb_minimap

    @property
    def bgr_minimap(self):
        self._prev_bgr_minimap = self._bgr_minimap
        self._bgr_minimap = self._minimap_cropper.crop_minimap(self.bgr_screen)
        return self._bgr_minimap

    @property
    def prev_bgr_minimap(self):
        return self._prev_rgb_minimap

    def get_masked_bgr_minimap(self, mask):
        return conv.get_masked_bgr_img(self._minimap_cropper.crop_minimap(self.bgr_screen),
                                       self.mask_mapping[mask])

    @property
    def minimap_cropper(self):
        return self._minimap_cropper
