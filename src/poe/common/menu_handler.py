from src.poe.screen.image_factory import ImageFactory
from src.utils.imaging import img_finder as imgf
from src.utils.math import coordinates as coord


class MenuNavigator:
    def __init__(self, app):
        self._app = app
        self.menu_images = ImageFactory.get_menu_images()
        self.menu_btn_switch = {
            'hideout': self.menu_images['hideout'],
            'part1': self.menu_images['part1'],
            'part2': self.menu_images['part2'],
            'epi': self.menu_images['epilogue'],
            '6': self.menu_images['act6'],
            '7': self.menu_images['act7'],
            '8': self.menu_images['act8'],
            '9': self.menu_images['act9'],
            '10': self.menu_images['act10'],
            'quarry': self.menu_images['quarry'],
        }

    def click_on_menu_btn(self, btn_name):
        img_box = imgf.get_template_img_location(self._app.bgr_screen,
                                                 self.menu_btn_switch[btn_name],
                                                 threshold=.95)
        if img_box is not None:
            img_pt = coord.get_centroid(img_box)
            self._app.inputs.click_on_coords(coords=(int(img_pt[0]), int(img_pt[1])))
            return True
        return False

    def drop_off_all_inventory(self):
        if self._app.imaging.wait_for_image_on_screen(self.menu_images['inventory']):
            r, c = 5, 11
            start_pt, end_pt = 1350, 650 # only works for 1920x1080
            interval = 55
            for col in range(c):
                for row in range(r):
                    pt1, pt2 = start_pt + (col * interval), end_pt + (row * interval)
                    self._app.inputs.click_on_coords(mouse='left',
                                                     coords=(pt1, pt2),
                                                     pressed='control')