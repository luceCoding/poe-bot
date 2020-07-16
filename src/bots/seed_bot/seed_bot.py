from src.poe.bot import poe_bot
from pynput import keyboard
from src.poe.common.config_manager import ConfigurationManager
import gc


class SeedBot():

    def __init__(self):
        self.bot = poe_bot.POEBot()
        self.break_program = False
        self.item_set = set([x.upper() for x in ConfigurationManager.get_item_config()['items']])

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            while not self.break_program:
                self.bot.app.inputs.close_all_menus()
                self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
                if not self.find_seeds() and not self.break_program:
                    if not self.restart_instance() and not self.break_program:
                        if not self.get_out_of_jail() and not self.break_program:
                            print('Stuck. Help!')
                            break #TODO
                elif not self.restart_instance() and not self.break_program:
                    if not self.get_out_of_jail() and not self.break_program:
                        print('Stuck. Help!')
                        break #TODO
                gc.collect()
            listener.join()

    def find_seeds(self):
        directions_in_degrees = [180, 270, 1, 45]
        for direction_in_degrees in directions_in_degrees:
            print('Direction: ', direction_in_degrees)
            if self.break_program:
                break
            if self.bot.explore_one_direction(minimap_pois=self.bot.images['minimap']['seed'],
                                              direction_in_degrees=direction_in_degrees,
                                              item_name_set=self.item_set,
                                              distance_from_poi=30,
                                              max_moves=6):
                if self.bot.pickup_item_by_image_matching(self.bot.images['objects']['grove'][0]):
                    if self.bot.pickup_items_by_ocr(item_set=self.item_set, max_items=7):
                        return True # done, found all the seeds
                else:
                    break
        return False

    def restart_instance(self):
        if not self.bot.is_in_town:
            if self.bot.go_to_waypoint(max_moves=13,
                                       distance_from_waypoint=30,
                                       item_set=self.item_set):
                if self.bot.open_nearby_waypoint_world_menu(drop_off=True,
                                                            drop_order=['seed_stockpile', 'stash']):
                    if self.bot.create_new_area_with_world_menu(self.bot.images['menu_btns']['quarry'][0]):
                        self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
                        return True
        return False

    def get_out_of_jail(self):
        if self.bot.open_town_portal():
            if self.bot.go_into_town_portal():
                if self.bot.open_nearby_waypoint_world_menu():
                    if self.bot.create_new_area_with_world_menu(self.bot.images['menu_btns']['quarry'][0]):
                        self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
                        return True
        return False

    def on_press(self, key):
        if key == keyboard.Key.end:
            print('end pressed')
            self.break_program = True
            return False

    # def test(self):
    #     self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
    #     if self.bot.go_into_town_portal():
    #         print('yes')
    #         if self.bot.open_nearby_waypoint_world_menu():
    #             print('success')
    #             return
    #     print('failed')