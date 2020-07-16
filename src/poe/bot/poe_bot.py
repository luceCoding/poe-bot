from src.poe.common.poe_app import POEApp
from src.utils.imaging import text_finder as txtf
from src.poe.screen.image_factory import ImageFactory
from src.utils.math import coordinates as coord
import time
import numpy as np
from src.poe.screen.image_handler import ImageHandler
from src.poe.common.menu_handler import MenuNavigator


class POEBot:

    def __init__(self):
        self.app = POEApp()
        self.images = ImageFactory.get_images()
        self.movement_distance = 400
        self.movement_delay = .4
        self.movement_variance = 100
        self.pickup_post_delay = .25  # based on if the item is right next to character
        self.n_actions = 0
        self.n_items_picked_up = 0
        self.action_stack = list()
        self.is_in_town = False
        self.img_handler = ImageHandler(self.app)
        self.menu_handler = MenuNavigator(self.app)

    def pickup_items_by_image_matching(self, imgs, max_items=10):
        picked_up, n_items = False, 0
        for img in imgs:
            while self.pickup_item_by_image_matching(img) and n_items < max_items:
                n_items += 1
                picked_up = True
        return picked_up

    def pickup_item_by_image_matching(self, img):
        img_coords = self.img_handler.find_img_pt_in_screen(img)
        if img_coords:
            print('Picking up item.')
            # self.app.inputs.left_click_on_coords(img_coords)
            # self.action_stack.append(img_coords)  # reset stack
            # time.sleep(self.pickup_post_delay)
            self.pickup_item(img_coords)
            return True
        return False

    def pickup_items_by_ocr(self, item_set, max_items=10):
        picked, n_items = False, 0
        while self.pickup_a_item_by_ocr(item_set) and n_items < max_items:
            n_items += 1
            picked = True
        return picked

    def pickup_a_item_by_ocr(self, item_set):
        self.app.update_screen()
        for text, pt1, pt2 in txtf.find_all_box_text_on_screen(self.app.bgr_screen):
            if len(text) >= 2 \
                    and (text[0].isdigit() or text[1].upper() == 'X'):  # deal with stacks of items
                text = ' '.join([x.strip().upper() for x in text.split(' ')[1:]])
            print('Found item: ', text)
            if text.upper() in item_set:
                print('Item pickup: ', text)
                coords = coord.get_centroid(np.array([pt1, pt2]))
                return self.pickup_item((int(coords[0]), int(coords[1])))
        return False

    def pickup_item(self,
                    coords,
                    sq_unit_size=90,
                    tick_per_sq_unit=.25):
        # distance_for_skill=100):
        distance = coord.calc_distance(coords, self.app.screen_center_pt)
        # if distance >= 150:
        #     self.app.inputs.button_skill(key='w', coords=coords)
        #     return True
        self.app.inputs.click_on_coords(coords=coords)
        self.action_stack.append(coords)
        self.n_items_picked_up += 1
        ticks = (distance + 1) // sq_unit_size
        # print('distance: ', distance)
        # print('ticks: ', ticks)
        # print(ticks * tick_per_sq_unit)
        # farther the item, the greater wait time
        time.sleep(self.pickup_post_delay + (ticks * tick_per_sq_unit))
        return True

    def take_one_step_to_fog(self, direction_in_degrees=None):  # [105,43,107]
        print('Going to fog.')
        if direction_in_degrees:
            radians = coord.degrees_to_radians(direction_in_degrees)
            coords = coord.calc_coords(self.app.screen_center_pt,
                                       self.movement_distance,
                                       radians)
            self.app.inputs.click_on_coords(coords=coords)
            self.app.inputs.button_skill('w', coords, variance=self.movement_variance)
            self.action_stack.append(coords)
            time.sleep(self.movement_delay)
            return True
        else:
            mini_distance, mini_radians = self.app.minimap_handler.get_closest_distance_and_radians_to_minimap_fog()
            if mini_distance and mini_radians:
                coords = coord.calc_coords(self.app.screen_center_pt,
                                           self.movement_distance,
                                           mini_radians)
                self.app.inputs.click_on_coords(coords=coords)
                self.app.inputs.button_skill('w', coords, variance=self.movement_variance)
                self.action_stack.append(coords)
                time.sleep(self.movement_delay)
                return True
        return False

    def open_town_portal(self):
        print('TP needed')
        self.app.inputs.open_inventory()
        if self.img_handler.wait_for_image_on_screen(self.images['menu_btns']['inventory'][0]):
            coords = self.img_handler.find_img_pt_in_screen(self.images['inventory']['town_portal'][0],
                                                            threshold=.6)
            if coords is not None:
                print('Opened Town portal.')
                self.app.inputs.mouse_skill(button='right', coords=coords)
                self.app.inputs.close_all_menus()
                time.sleep(.25)
                return True
        print('Can\'t find town portal.')
        return False

    def go_into_town_portal(self):
        print('Going into town portal.')
        self.action_stack = list()
        if self.img_handler.wait_for_image_on_screen(self.images['objects']['highgate'][0]):
            coords = self.img_handler.find_img_pt_in_screen(self.images['objects']['highgate'][0])
            if coords is not None:
                print('Went into town portal.')
                self.app.inputs.click_on_coords(coords=coords)
                self.is_in_town = True
                time.sleep(.5)
                return True
        print('Can\'t find town portal.')
        return False

    def open_nearby_waypoint_world_menu(self, drop_off=False, drop_order=[]):
        print('Opening world menus.')
        print('n_items: ', self.n_items_picked_up)
        if drop_off \
                and self.n_items_picked_up >= 300 \
                and self.menu_handler.open_object('waypoint'):
            if self.menu_handler.click_on_menu_btn('hideout'):
                for obj in drop_order:
                    if self.menu_handler.open_object(obj):
                        self.menu_handler.drop_off_all_inventory()
                        self.app.inputs.close_all_menus()
                        print('Opened: ', obj)
                    else:
                        return False
                self.n_items_picked_up = 0
                # go back to instance
                if self.menu_handler.open_object('waypoint'):
                    menu_btns = ['part2'] # TODO, add when in part already
                    for btn in menu_btns:
                        if not self.menu_handler.click_on_menu_btn(btn):
                            return False
                return True
        elif self.menu_handler.open_object('waypoint'):
            print('Opened world menu')
            return True
        return False

    def create_new_area_with_world_menu(self, area_menu_btn):
        print('Create new instance.')
        area_menu_coords = self.img_handler.find_img_pt_in_screen(area_menu_btn)
        if area_menu_coords:
            self.app.inputs.click_on_coords(coords=area_menu_coords, pressed='control')
            if self.img_handler.wait_for_image_on_screen(self.images['menu_btns']['instance_manager'][0],
                                                         threshold=.7):
                if self.app.try_click_on_image(self.images['menu_btns']['new_instance_btn'][0]):
                    self.is_in_town = False
                    self.action_stack = list()
                    return self.img_handler.wait_for_image_on_screen(self.images['objects']['waypoint'][0],
                                                                     post_delay=2)
        return False

    def go_to_waypoint(self,
                       max_moves=25,
                       distance_from_waypoint=50,
                       item_set=None):
        print('Going back to waypoint.')
        n_moves = 0
        while len(self.action_stack) and n_moves < max_moves:
            n_moves += 1
            if self.app.minimap_handler.find_any_pts_on_minimap(
                    self.images['minimap']['waypoint']) is not None:  # backtrack to waypoint
                coords, mini_distance = self.app.minimap_handler.get_coords_and_distance_in_minimap(
                    self.images['minimap']['waypoint'])
                if coords:
                    if mini_distance and mini_distance <= distance_from_waypoint:
                        return True  # nearby waypoint
                    self.app.inputs.click_on_coords(coords=coords)
                    self.app.inputs.button_skill('w', coords, variance=self.movement_variance)
                    self.action_stack.append(coords)
                    time.sleep(self.movement_delay)
                    if item_set:
                        self.pickup_items_by_ocr(item_set)
                    continue
            prev_coords = self.action_stack.pop()
            inverse_coords = coord.inverse_pts_on_pivot(self.app.screen_center_pt, prev_coords)
            self.app.inputs.click_on_coords(coords=inverse_coords)
            self.app.inputs.button_skill('w', inverse_coords)
            time.sleep(self.movement_delay)
            if item_set:
                self.pickup_items_by_ocr(item_set)
        return False

    def explore_one_direction(self,
                              minimap_pois,
                              direction_in_degrees=None,
                              item_name_set=None,
                              distance_from_poi=50,
                              max_moves=25):
        n_moves = 0
        while n_moves < max_moves:
            n_moves += 1
            coords, mini_distance = self.app.minimap_handler.get_coords_and_distance_in_minimap(minimap_pois)
            if coords and mini_distance:
                if mini_distance <= distance_from_poi:  # we are nearby
                    return True
                self.app.inputs.click_on_coords(coords=coords)
                self.app.inputs.button_skill('w', coords, variance=self.movement_variance)  # move towards POI
                self.action_stack.append(coords)
                time.sleep(self.movement_delay)
            elif not self.take_one_step_to_fog(direction_in_degrees):
                return False  # failed to find anything
            if item_name_set:
                self.pickup_a_item_by_ocr(item_name_set)
        return False
