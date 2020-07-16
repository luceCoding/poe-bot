from src.poe.screen.image_factory import ImageFactory
from src.utils.imaging import img_finder as imgf
from src.utils.math import coordinates as coord
from src.poe.screen.image_handler import ImageHandler


class MenuNavigator:
    def __init__(self, app):
        self.app = app
        self.menu_images = ImageFactory.get_menu_images()
        self.obj_images = ImageFactory.get_object_images()
        self.img_handler = ImageHandler(self.app)

    def click_on_menu_btn(self, btn_name):
        switch = {
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
        self.app.update_screen()
        img_box = imgf.get_template_img_location(self.app.bgr_screen,
                                                 switch[btn_name],
                                                 threshold=.95)
        if img_box is not None:
            img_pt = coord.get_centroid(img_box)
            self.app.inputs.click_on_coords(coords=(int(img_pt[0]), int(img_pt[1])))
            return True
        return False

    def open_object(self, object_name):
        switch = {
            'waypoint': (self.obj_images['waypoint'],
                         self.obj_images['waypoint_post']),
            'stash': (self.obj_images['stash'],
                      self.obj_images['stash_post']),
            'seed_stockpile': (self.obj_images['seed_stockpile'],
                               self.obj_images['seed_stockpile_post']),
        }
        self.app.update_screen()
        if self.img_handler.wait_for_image_on_screen(switch[object_name][0]):
            img_box = imgf.get_template_img_location(self.app.bgr_screen,
                                                     switch[object_name][0],
                                                     threshold=.5)
            if img_box is not None:
                img_pt = coord.get_centroid(img_box)
                self.app.inputs.click_on_coords(coords=(int(img_pt[0]), int(img_pt[1])))
                if self.img_handler.wait_for_image_on_screen(switch[object_name][1]):
                    return True
        return False

    def drop_off_all_inventory(self):
        if self.img_handler.wait_for_image_on_screen(self.menu_images['inventory']):
            r, c = 5, 11
            start_pt, end_pt = 1350, 650 # only works for 1920x1080
            interval = 55
            for col in range(c):
                for row in range(r):
                    pt1, pt2 = start_pt + (col * interval), end_pt + (row * interval)
                    self.app.inputs.click_on_coords(mouse='left',
                                                    coords=(pt1, pt2),
                                                    pressed='control')