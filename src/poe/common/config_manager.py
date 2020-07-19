import yaml
import pkg_resources
import os

resource_pkg = pkg_resources.get_distribution('poe_bot').location


class ConfigurationManager:

    @staticmethod
    def get_item_config():
        with open(os.path.join(resource_pkg, './configs/items.yaml'),
                  'rt',
                  encoding='utf8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def get_mask_config():
        with open(os.path.join(resource_pkg, './configs/masks.yaml')) as f:
            return yaml.safe_load(f)
