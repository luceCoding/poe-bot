import cv2
from glob import glob
from collections import defaultdict
import pkg_resources
import os

resource_pkg = pkg_resources.get_distribution('poe_bot').location
img_dir = os.path.join(resource_pkg, 'resources/images')


class ImageFactory(dict):

    @staticmethod
    def get_images():
        d = defaultdict(lambda: defaultdict(list))
        for p in glob(os.path.join(img_dir, 'inventory/town_portal/town_portal*.png')):
            d['inventory']['town_portal'].append(cv2.imread(p))

        for p in glob(os.path.join(img_dir, 'menu/new_instance/*.png')):
            d['menu_btns']['new_instance_btn'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'menu/quarry/quarry.png')):
            d['menu_btns']['quarry'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'menu/world/world.png')):
            d['menu_btns']['world'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'menu/instance_manager/instance_manager.png')):
            d['menu_btns']['instance_manager'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'menu/inventory/inventory.png')):
            d['menu_btns']['inventory'].append(cv2.imread(p))

        for p in glob(os.path.join(img_dir, 'minimap/player/*.png')):
            d['minimap']['player'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'minimap/seed/*.png')):
            d['minimap']['seed'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'minimap/waypoint/*.png')):
            d['minimap']['waypoint'].append(cv2.imread(p))

        for p in glob(os.path.join(img_dir, 'objects/waypoint/*.png')):
            d['objects']['waypoint'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'objects/highgate/highgate*.png')):
            d['objects']['highgate'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'objects/grove/sacred_grove.png')):
            d['objects']['grove'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'objects/quarry/quarry.png')):
            d['objects']['quarry'].append(cv2.imread(p))
        return d
