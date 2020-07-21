from src.poe.controls.poe_app import POEApp
from src.utils.imaging import text_finder as txtf
from src.poe.screen.image_factory import ImageFactory
from src.utils.math import coordinates as coord
import time
import numpy as np
from src.poe.common.menu_handler import MenuNavigator
from src.poe.common.object_handler import ObjectHandler
from src.poe.common.navigation import inventory
from abc import ABCMeta, abstractmethod
import logging
from src.poe.common.navigation import world_menu


class POEBot(metaclass=ABCMeta):

    def __init__(self):
        self.app = POEApp()
        self.images = ImageFactory.get_images()
        self.movement_distance = 400
        self.movement_delay = .4
        self.movement_variance = 50
        self.pickup_post_delay = .25  # based on if the item is right next to character
        self.n_actions = 0
        self.n_items_picked_up = 0
        self.action_stack = list()
        self.is_in_town = False
        self.menu_handler = MenuNavigator(self.app)
        self.obj_handler = ObjectHandler(self.app)
        self.movement_key = 'w'

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def buff_up(selfs):
        raise NotImplementedError

    def pickup_item_by_image_matching(self, img):
        img_coords = self.app.imaging.get_center_point_of_image_in_screen(img)
        if img_coords:
            self.pickup_item(img_coords)
            return True
        return False

    def pickup_items_by_ocr(self, item_set, max_items=10):
        picked = False
        for _ in range(max_items):
            if self.pickup_a_item_by_ocr(item_set):
                picked = True
            else:
                break
        return picked

    def pickup_a_item_by_ocr(self, item_set):
        # self.app.update_screen()
        screen = self.app.bgr_screen
        for text, pt1, pt2 in txtf.find_all_box_text_on_image(screen):
            # deal with stacks of items
            if len(text) >= 2 and (text[0].isdigit() or text[1].upper() == 'X'):
                text = ' '.join([x.strip().upper() for x in text.split(' ')[1:]])
            logging.info('Found item: %s', text)
            if text.upper() in item_set:
                coords = coord.get_centroid(np.array([pt1, pt2]))
                return self.pickup_item((int(coords[0]), int(coords[1])))
        del screen
        return False

    def pickup_item(self,
                    coords,
                    sq_unit_size=90,
                    tick_per_sq_unit=.25):
        distance = coord.calc_distance(coords, self.app.screen_center_pt)
        logging.info('Picked up item.')
        self.app.inputs.click_on_coords(coords=coords)
        self.action_stack.append(coords)
        self.n_items_picked_up += 1
        ticks = (distance + 1) // sq_unit_size
        time.sleep(self.pickup_post_delay + (ticks * tick_per_sq_unit))
        return True  # TODO: perform jump for farther items

    def take_one_step_to_fog(self, direction_in_degrees=None):
        if direction_in_degrees:
            return self.move_to_direction(direction_in_degrees)
        else:
            mini_distance, mini_radians = self.app.minimap_handler.get_closest_distance_and_radians_to_minimap_fog()
            if mini_distance and mini_radians:
                logging.info('Going to fog.')
                coords = coord.calc_coords(self.app.screen_center_pt,
                                           self.movement_distance,
                                           mini_radians)
                self.app.inputs.click_on_coords(coords=coords)
                self.app.inputs.button_skill(self.movement_key,
                                             coords,
                                             variance=self.movement_variance)
                self.action_stack.append(coords)
                time.sleep(self.movement_delay)
                return True
        return False

    def move_to_direction(self, direction_in_degrees):
        logging.info('Going to direction: %s', direction_in_degrees)
        radians = coord.degrees_to_radians(direction_in_degrees)
        coords = coord.calc_coords(self.app.screen_center_pt,
                                   self.movement_distance,
                                   radians)
        self.app.inputs.click_on_coords(mouse='middle', coords=coords, double=True)
        self.app.inputs.button_skill(self.movement_key,
                                     coords,
                                     variance=self.movement_variance)
        self.action_stack.append(coords)
        time.sleep(self.movement_delay)
        return True

    def open_town_portal(self):
        logging.info('TP needed')
        with inventory(self):
            if self.app.click_on_image_and_wait_for(self.images['inventory']['town_portal'][0],
                                                    self.images['objects']['highgate'][0],
                                                    mouse='right',
                                                    second_threshold=.5):
                logging.info('Opened town portal.')
                return True
        logging.warning('Can\'t find town portal.')
        return False

    def go_into_town_portal(self):
        logging.info('Going into town portal.')
        if self.app.click_on_image_and_wait_for(self.images['objects']['highgate'][0],
                                                self.images['objects']['waypoint'][0]):
            del self.action_stack
            self.action_stack = list()
            logging.info('Returned to town.')
            return True
        logging.info('Can\'t find town portal.')
        return False

    def create_new_area_with_world_menu(self, area_menu_btn):
        logging.info('Create new instance.')
        with world_menu(self, movement_delay=1):
            self.menu_handler.click_on_world_menu_btn('part2')
            time.sleep(.1)
            self.menu_handler.click_on_world_menu_btn('act9')
            time.sleep(.1)
            if self.app.click_on_image_and_wait_for(area_menu_btn,
                                                    self.images['menu_btns']['instance_manager'][0],
                                                    pressed='control'):
                if self.app.click_on_image_and_wait_for(self.images['menu_btns']['new_instance_btn'][0],
                                                        self.images['objects']['waypoint'][0]):
                    del self.action_stack
                    self.action_stack = list()
                    return True
        return False

    def go_to_waypoint(self,
                       max_moves=15,
                       distance_from_waypoint=25,
                       movement_delay=None):
        if movement_delay is None:
            movement_delay = self.movement_delay
        logging.info('Going back to waypoint')
        for _ in range(max_moves):
            coords, mini_distance = self.app.minimap_handler.get_coords_and_distance_in_minimap(
                self.images['minimap']['waypoint'])
            if coords is not None:
                if mini_distance and mini_distance <= distance_from_waypoint:
                    logging.info('Near waypoint.')
                    return True  # nearby waypoint
                self.app.inputs.move_mouse(coords=coords)
                self.app.inputs.click_on_coords(coords=coords, mouse='middle', double=True)
                self.app.inputs.button_skill(self.movement_key,
                                             coords,
                                             variance=self.movement_variance)
                self.action_stack.append(coords)
                time.sleep(movement_delay)
            elif len(self.action_stack):
                prev_coords = self.action_stack.pop()
                inverse_coords = coord.inverse_pts_on_pivot(self.app.screen_center_pt, prev_coords)
                self.app.inputs.click_on_coords(coords=inverse_coords)
                self.app.inputs.button_skill(self.movement_key,
                                             inverse_coords)
                time.sleep(movement_delay)
        return False

    def explore_one_direction(self,
                              minimap_pois,
                              direction_in_degrees=None,
                              item_name_set=None,
                              distance_from_poi=25,
                              max_moves=25):
        for _ in range(max_moves):
            coords, mini_distance = self.app.minimap_handler.get_coords_and_distance_in_minimap(minimap_pois)
            if coords is not None and mini_distance is not None:
                if mini_distance <= distance_from_poi:
                    return True  # we are nearby poi
                self.app.inputs.click_on_coords(coords=coords, double=True)
                self.app.inputs.button_skill(self.movement_key,
                                             coords,
                                             variance=self.movement_variance)  # move towards POI
                self.action_stack.append(coords)
                time.sleep(self.movement_delay)
            elif not self.take_one_step_to_fog(direction_in_degrees):
                return False  # failed to find anything
            if item_name_set:
                self.pickup_a_item_by_ocr(item_name_set)
        return False

    def drop_off_inventory_items(self):
        with world_menu(self):
            if not self.menu_handler.click_on_world_menu_btn('hideout'):
                return False
        actions = [self.obj_handler.open_object('seed_stockpile'),
                   self.menu_handler.drop_off_all_inventory(),
                   self.app.inputs.close_all_menus(),
                   self.obj_handler.open_object('stash'),
                   self.menu_handler.drop_off_all_inventory(),
                   self.app.inputs.close_all_menus()]
        return all(actions)
