import cv2
from glob import glob
from collections import defaultdict


class ImageFactory(dict):

    @staticmethod
    def get_images():
        d = defaultdict(lambda: defaultdict(list))
        for p in glob('./images/inventory/town_portal/town_portal*.png'):
            d['inventory']['town_portal'].append(cv2.imread(p))

        for p in glob('./images/items/sacred_grove.png'):
            d['items']['grove'].append(cv2.imread(p))

        for p in glob('./images/items/seed.png'):
            d['items']['loot'].append(cv2.imread(p))
        for p in glob('./images/items/orbs.png'):
            d['items']['loot'].append(cv2.imread(p))

        for p in glob('./images/menu/new_instance/*.png'):
            d['menu_btns']['new_instance_btn'].append(cv2.imread(p))
        for p in glob('./images/menu/quarry/quarry.png'):
            d['menu_btns']['quarry'].append(cv2.imread(p))
        for p in glob('./images/menu/world/world.png'):
            d['menu_btns']['world'].append(cv2.imread(p))

        for p in glob('./images/minimap/player/*.png'):
            d['minimap']['player'].append(cv2.imread(p))
        for p in glob('./images/minimap/seed/*.png'):
            d['minimap']['seed'].append(cv2.imread(p))
        for p in glob('./images/minimap/waypoint/*.png'):
            d['minimap']['waypoint'].append(cv2.imread(p))

        for p in glob('./images/objects/waypoint/*.png'):
            d['objects']['waypoint'].append(cv2.imread(p))
        for p in glob('./images/objects/highgate/highgate*.png'):
            d['objects']['highgate'].append(cv2.imread(p))

        print(len(d['items']['loot']))

        return d

# town porta - [106 212 160]