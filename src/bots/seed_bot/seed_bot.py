from src.poe.bot.poe_bot import POEBot
from src.poe.common.config_manager import ConfigurationManager
from src.poe.common.navigation import main_rotation
import logging


class SeedBot(POEBot):

    def __init__(self):
        super(SeedBot, self).__init__()
        self.item_set = set([x.upper() for x in ConfigurationManager.get_item_config()['items']])
        self.dir_and_steps = zip([180, 270, 315, 45], [4, 3, 6, 6])

    def run(self):
        with main_rotation(self):
            self.new_instance()
            self.buff_up()
            self.find_seeds()

    def drop_off(self):
        with main_rotation(self):
            self.drop_off_inventory_items()

    def buff_up(self):
        self.app.inputs.mouse_skill(button='right')  # cast righteous fire

    def find_seeds(self):
        for direction, steps in self.dir_and_steps:
            if self.explore_one_direction(minimap_pois=self.images['minimap']['seed'],
                                          direction_in_degrees=direction,
                                          item_name_set=self.item_set,
                                          distance_from_poi=35,
                                          max_moves=steps):
                if self.pickup_item_by_image_matching(self.images['objects']['grove'][0]):
                    if self.pickup_items_by_ocr(item_set=self.item_set, max_items=7):
                        return True  # done, found all the seeds
        return False

    def new_instance(self):
        return self.create_new_area_with_world_menu(self.images['menu_btns']['quarry'][0])

    def go_to_character_selection(self):
        if self.menu_handler.click_on_esc_menu_btn('character_selection'):
            logging.info('Going to character selection.')
            self.action_stack = list()
            return True
        return False

    def get_out_of_jail(self):
        if self.open_town_portal():
            return self.go_into_town_portal()
        return False
