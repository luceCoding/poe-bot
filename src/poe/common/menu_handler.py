from src.poe.screen.image_factory import ImageFactory
from src.utils.imaging import img_finder as imgf
from src.utils.math import coordinates as coord
import logging


class MenuNavigator:
    def __init__(self, app):
        self._app = app
        self.menu_images = ImageFactory.get_menu_images()
        self.menu_btn_switch = {
            'hideout': self.menu_images['hideout'],
            'part1': self.menu_images['part1'],
            'part2': self.menu_images['part2'],
            'epi': self.menu_images['epilogue'],
            'act6': self.menu_images['act6'],
            'act7': self.menu_images['act7'],
            'act8': self.menu_images['act8'],
            'act9': self.menu_images['act9'],
            'act10': self.menu_images['act10'],
            'quarry': self.menu_images['quarry'],
        }
        self.esc_btn_switch = {
            'character_selection': self.menu_images['character_selection'],
        }
        self.character_selection_switch = {
            'play': self.menu_images['play']
        }

    def click_on_world_menu_btn(self, btn_name):
        img_box = imgf.get_template_img_location(self._app.bgr_screen,
                                                 self.menu_btn_switch[btn_name],
                                                 threshold=.95)
        if img_box is not None:
            img_pt = coord.get_centroid(img_box)
            self._app.inputs.click_on_coords(coords=(int(img_pt[0]), int(img_pt[1])))
            return True
        return False

    def click_on_esc_menu_btn(self, btn_name, max_tries=5):
        logging.info('Open ESC menu.')
        for _ in range(max_tries):
            self._app.inputs.open_esc_menu()
            if self._app.imaging.wait_for_image_on_screen(self.esc_btn_switch[btn_name],
                                                          threshold=.7):
                self._app.click_on_image_once(self.esc_btn_switch[btn_name],
                                              threshold=.7)
                if not self._app.imaging.wait_for_image_on_screen(self.esc_btn_switch[btn_name],
                                                                  max_tries=1,
                                                                  threshold=.7):
                    return True
            self._app.inputs.close_all_menus()
        return False

    def click_on_character_menu_btn(self, btn_name, max_tries=5):
        for _ in range(max_tries):
            if self._app.imaging.wait_for_image_on_screen(self.character_selection_switch[btn_name],
                                                          threshold=.7):
                self._app.click_on_image_once(self.character_selection_switch[btn_name],
                                              threshold=.7)
                if not self._app.imaging.wait_for_image_on_screen(self.character_selection_switch[btn_name],
                                                                  max_tries=1,
                                                                  threshold=.7):
                    return True
        return False

    def drop_off_all_inventory(self):
        if self._app.imaging.wait_for_image_on_screen(self.menu_images['inventory']):
            r, c = 5, 12
            start_pt, end_pt = 1300, 650  # only works for 1920x1080
            interval = 55
            for col in range(c):
                for row in range(r):
                    pt1, pt2 = start_pt + (col * interval), end_pt + (row * interval)
                    self._app.inputs.click_on_coords(mouse='left',
                                                     coords=(pt1, pt2),
                                                     pressed='control')
