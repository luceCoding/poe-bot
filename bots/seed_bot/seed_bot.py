from poe.bot import poebot
from pynput import keyboard


class SeedBot():

    def __init__(self):
        self.cache_name_set = set([_.upper() for _ in ['sacred', 'grove', 'seed']])
        self.loot_name_set = set([_.upper() for _ in ['wild', 'vivid', 'primal', 'seed', 'orb']])
        self.bot = poebot.POEBot()
        self.break_program = False

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            while not self.break_program:
                if not self.find_seeds():
                    self.get_out_of_jail()
                    self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
            listener.join()

    def find_seeds(self):
        self.bot.app.inputs.close_all_menus()
        self.bot.app.inputs.mouse_skill(button='right')  # cast righteous fire
        for direction in range(3):
            if self.break_program:
                break
            if self.bot.explore_one_direction(pivot=self.bot.images['minimap']['waypoint'],
                                              minimap_pois=self.bot.images['minimap']['seed'],
                                              item_imgs=self.bot.images['items']['loot'],
                                              # item_name_set=self.loot_name_set,
                                              distance_from_poi=40,
                                              max_moves=10):
                # if self.bot.pickup_items_by_text_matching(self.cache_name_set, [120, 120, 247]):
                #     if self.bot.pickup_items_by_text_matching(self.loot_name_set, [0, 255, 254]):
                #         break  # done, found the seeds, go back to waypoint
                if self.bot.pickup_item_by_image_matching(self.bot.images['items']['grove'][0]):
                    if self.bot.pickup_items_by_image_matching(self.bot.images['items']['loot']):
                        break  # done, found the seeds, go back to waypoint
                break
            elif not self.bot.go_back_to_waypoint(max_moves=11,
                                                  distance_from_waypoint=40):  # go back to waypoint
                print('tp1')
                break
        if not self.bot.is_in_town:
            if self.bot.go_back_to_waypoint(max_moves=11,
                                            distance_from_waypoint=40):
                if self.bot.find_waypoint_box_on_screen() is not None:
                    if self.bot.open_nearby_waypoint_world_menu():
                        if self.bot.create_new_instance_with_world_menu(self.bot.images['menu_btns']['quarry'][0]):
                            return True
            print('tp2')
        return False

    def get_out_of_jail(self):
        if self.bot.open_town_portal():
            if self.bot.go_to_town():
                self.bot.wait_for_loading_area()
                if self.bot.open_nearby_waypoint_world_menu():
                    self.bot.wait_for_world_menu()
                    if self.bot.create_new_instance_with_world_menu(self.bot.images['menu_btns']['quarry'][0]):
                        return True
        return False

    def on_press(self, key):
        if key == keyboard.Key.end:
            print('end pressed')
            self.break_program = True
            return False


s = SeedBot()
s.start()
