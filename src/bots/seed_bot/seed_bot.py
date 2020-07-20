from src.poe.bot.poe_bot import POEBot
from src.poe.common.config_manager import ConfigurationManager
from src.poe.common.navigation import waypoint
from src.poe.common.navigation import world_menu
import gc
import logging


class SeedBot(POEBot):

    def __init__(self):
        super(SeedBot, self).__init__()
        self.item_set = set([x.upper() for x in ConfigurationManager.get_item_config()['items']])

    def run(self):
        with waypoint(self):
            self.buff_up()
            self.find_seeds()
        self.restart_instance()
        logging.debug('Garbage: {}'.format(gc.garbage))
        logging.debug('Tracked objects: {}'.format(*gc.get_objects()))

    def buff_up(self):
        self.app.inputs.mouse_skill(button='right')  # cast righteous fire

    def find_seeds(self):
        directions_in_degrees = [180, 270, 1, 45]
        for direction_in_degrees in directions_in_degrees:
            if self.explore_one_direction(minimap_pois=self.images['minimap']['seed'],
                                          direction_in_degrees=direction_in_degrees,
                                          item_name_set=self.item_set,
                                          distance_from_poi=25,
                                          max_moves=6):
                if self.pickup_item_by_image_matching(self.images['objects']['grove'][0]):
                    if self.pickup_items_by_ocr(item_set=self.item_set, max_items=7):
                        return True  # done, found all the seeds
        return False

    def restart_instance(self):
        return self.create_new_area_with_world_menu(self.images['menu_btns']['quarry'][0])

    def get_out_of_jail(self):
        if self.open_town_portal():
            return self.go_into_town_portal()
        return False

    # def test(self):
    #     with keyboard.Listener(on_press=self.on_press) as listener:
    #         while not self.break_program:
    #             self.pickup_items_by_ocr(item_set=self.item_set, max_items=7)
    #             gc.collect()
    #     listener.join()
