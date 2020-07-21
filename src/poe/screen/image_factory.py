import cv2
from glob import glob
from collections import defaultdict
import pkg_resources
import os

resource_pkg = pkg_resources.get_distribution('poe_bot').location
img_dir = os.path.join(resource_pkg, 'resources/images')


class ImageFactory:

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

        # for p in glob(os.path.join(img_dir, 'minimap/player/*.png')):
        #     d['minimap']['player'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'minimap/seed/seed*.png')):
            d['minimap']['seed'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'minimap/waypoint/*.png')):
            d['minimap']['waypoint'].append(cv2.imread(p))
        # _ = os.path.join(img_dir, 'menu/stash/stash_obj.png')
        # d['minimap']['stash'].append(cv2.imread(_))

        for p in glob(os.path.join(img_dir, 'objects/waypoint/*.png')):
            d['objects']['waypoint'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'objects/highgate/highgate*.png')):
            d['objects']['highgate'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'objects/grove/sacred_grove.png')):
            d['objects']['grove'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'objects/quarry/quarry.png')):
            d['objects']['quarry'].append(cv2.imread(p))
        for p in glob(os.path.join(img_dir, 'objects/stash/stash.png')):
            d['objects']['stash'].append(cv2.imread(p))
        return d

    @staticmethod
    def get_menu_images():
        d = defaultdict()
        _ = os.path.join(img_dir, 'menu/new_instance/new_instance_btn.png')
        d['new_instance_btn'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/quarry/quarry.png')
        d['quarry'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'objects/waypoint/world.png')
        d['world'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/instance_manager/instance_manager.png')
        d['instance_manager'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/inventory/inventory.png')
        d['inventory'] = cv2.imread(_)

        _ = os.path.join(img_dir, 'menu/world/act6_btn.png')
        d['act6'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/world/act7_btn.png')
        d['act7'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/world/act8_btn.png')
        d['act8'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/world/act9_btn.png')
        d['act9'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/world/act10_btn.png')
        d['act10'] = cv2.imread(_)

        _ = os.path.join(img_dir, 'menu/hideout/hideout.png')
        d['hideout'] = cv2.imread(_)

        _ = os.path.join(img_dir, 'menu/world/part1.png')
        d['part1'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/world/part2.png')
        d['part2'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/world/epilogue.png')
        d['epilogue'] = cv2.imread(_)

        _ = os.path.join(img_dir, 'menu/character_selection/character_selection.png')
        d['character_selection'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'menu/character_selection/play.png')
        d['play'] = cv2.imread(_)

        return d

    @staticmethod
    def get_object_images():
        d = defaultdict()
        _ = os.path.join(img_dir, 'objects/waypoint/waypoint1.png')
        d['waypoint'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'objects/seed_stockpile/seed_stockpile.png')
        d['seed_stockpile'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'objects/stash/stash.png')
        d['stash'] = cv2.imread(_)

        _ = os.path.join(img_dir, 'objects/waypoint/world.png')
        d['waypoint_post'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'objects/seed_stockpile/seed_stockpile_post.png')
        d['seed_stockpile_post'] = cv2.imread(_)
        _ = os.path.join(img_dir, 'objects/stash/stash_post.png')
        d['stash_post'] = cv2.imread(_)
        return d