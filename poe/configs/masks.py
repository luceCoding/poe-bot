import yaml

class MaskManager(dict):

    def __init__(self):
        with open('./configs/masks.yaml') as f:
            self.masks = yaml.safe_load(f)
        self.switch = {
            'fog': self.masks['fog_hsv_mask']['mask'],
            'wall': self.masks['wall_hsv_mask']['mask'],
            'waypoint': self.masks['waypoint_hsv_mask']['mask']
        }

    def __getitem__(self, item):
        return self.switch.get(item, None)