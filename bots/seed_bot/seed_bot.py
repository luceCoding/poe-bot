from poe.bot import poebot
from pynput import keyboard
import yaml


class SeedBot():

    def __init__(self):
        self.cache_name_set = set([_.upper() for _ in ['sacred', 'grove', 'seed']])
        self.loot_name_set = set([_.upper() for _ in ['wild', 'vivid', 'primal', 'seed', 'orb']])
        self.bot = poebot.POEBot()
        self.break_program = False
        with open('./configs/items.yaml') as f:
            data = yaml.safe_load(f)
        self.item_set = set([x.upper() for x in data['items']])
        # print(self.item_set)

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            # if not self.restart_instance():
            #     print('Put me near a waypoint sir.')
            #     return
            while not self.break_program:
                if not self.find_seeds():
                    if not self.get_out_of_jail():
                        print('Stuck. Help!')
                        break #TODO
                elif not self.restart_instance():
                    if not self.get_out_of_jail():
                        print('Stuck. Help!')
                        break #TODO
            listener.join()

    def find_seeds(self):
        self.bot.app.inputs.close_all_menus()
        self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
        directions_in_degrees = [180, 270, 1, 45]
        for direction_in_degrees in directions_in_degrees:
            print('Direction: ', direction_in_degrees)
            if self.break_program:
                break
            if self.bot.explore_one_direction(minimap_pois=self.bot.images['minimap']['seed'],
                                              item_imgs=self.bot.images['items']['loot'],
                                              direction_in_degrees=direction_in_degrees,
                                              item_name_set=self.item_set,
                                              distance_from_poi=30,
                                              max_moves=6):
                # if self.bot.pickup_items_by_text_matching(self.cache_name_set, [120, 120, 247]):
                #     if self.bot.pickup_items_by_text_matching(self.loot_name_set, [0, 255, 254]):
                #         break  # done, found the seeds, go back to waypoint
                # if self.bot.pickup_item_by_image_matching(self.bot.images['items']['grove'][0]):
                #     if self.bot.pickup_items_by_image_matching(self.bot.images['items']['loot']):
                #         break  # done, found the seeds, go back to waypoint
                if self.bot.pickup_item_by_image_matching(self.bot.images['items']['grove'][0]):
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
                                       # item_imgs=self.bot.images['items']['loot']):
                if self.bot.find_waypoint_box_on_screen() is not None:
                    if self.bot.open_nearby_waypoint_world_menu():
                        if self.bot.create_new_instance_with_world_menu(self.bot.images['menu_btns']['quarry'][0]):
                            self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
                            return True
        return False

    def get_out_of_jail(self):
        if self.bot.open_town_portal():
            if self.bot.go_to_town():
                self.bot.wait_for_loading_area()
                if self.bot.open_nearby_waypoint_world_menu():
                    self.bot.wait_for_world_menu()
                    if self.bot.create_new_instance_with_world_menu(self.bot.images['menu_btns']['quarry'][0]):
                        self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
                        return True
        return False

    def on_press(self, key):
        if key == keyboard.Key.end:
            print('end pressed')
            self.break_program = True
            return False

    # def test(self):
    #     # print(item_set)
    #     self.bot.app.update_screen()
    #     self.bot.find_seed_cache_by_ocr()

    def test(self):
        self.bot.app.update_screen()
        self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
        self.bot.pickup_items_by_ocr(self.item_set)


s = SeedBot()
# s.test()
s.start()
