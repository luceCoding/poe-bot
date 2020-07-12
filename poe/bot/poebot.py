from poe.screen.poeapp import POEApp
from utils.imaging import img_finder as imgf
from utils.imaging import text_finder as txtf
from utils.imaging import conversions as conv
from poe.screen.images import ImageFactory
from poe.common import movement as mv
from utils.math import coordinates as coord
import time


class POEBot:

    def __init__(self):
        self.app = POEApp()
        self.images = ImageFactory.get_images()
        self.movement_distance = 450
        self.movement_delay = .5
        self.pickup_delay = 1.5
        self.minimap_center_pt = (self.app.minimap_cropper.mid_x, self.app.minimap_cropper.mid_y)
        self.n_actions = 0
        self.n_items_picked_up = 0
        self.action_stack = list()
        self.is_in_town = False

    def find_img_in_minimap(self, img_to_find, threshold=.6):
        self.app.update_screen()
        coords = mini_distance = None
        box_pts = imgf.get_template_img_location(self.app.bgr_minimap, img_to_find, threshold)
        if box_pts is not None:  # found target
            center_img_pt = coord.get_centroid(box_pts)
            mini_distance, mini_radians = mv.calc_mini_movement(self.app.get_masked_bgr_minimap('wall'),
                                                                start_pt=self.minimap_center_pt,
                                                                end_pt=center_img_pt)

            coords = coord.calc_coords(self.app.screen_center_pt,
                                       self.movement_distance,
                                       mini_radians)
        return coords, mini_distance

    def find_img_in_screen(self, bgr_img, threshold=.6):
        self.app.update_screen()
        box_pts = imgf.get_template_img_location(self.app.bgr_screen, bgr_img, threshold)
        # print(box_pts)
        if box_pts is not None:
            center_img_pt = coord.get_centroid(box_pts)
            # import cv2
            # cv2.rectangle(self.app.bgr_screen,
            #               (box_pts[1][0], box_pts[1][1]),
            #               (box_pts[0][0], box_pts[0][1]),
            #               color=(0, 0, 255),
            #               thickness=2)
            # cv2.imshow("img", self.app.bgr_screen)
            # cv2.waitKey(0)
            return (int(center_img_pt[0]), int(center_img_pt[1]))
        return None

    def pickup_items_by_text_matching(self, name_set, hsv_color, offsets=[10, 10, 40]):
        picked_up = False
        text_data = self.get_text_data_on_screen_with(hsv_color)
        items_found = [x for x in text_data['text'] if x in name_set]
        print('items: ', items_found)
        for _ in range(len(items_found)):
            if self.pickup_item_by_text_matching(text_data, name_set):
                picked_up = True
                # self.app.update_screen()
                # item_mask = conv.get_masked_bgr_img(self.app.bgr_screen, hsv_color)
                # text_data = txtf.find_text_data(item_mask)
                text_data = self.get_text_data_on_screen_with(hsv_color)
        return picked_up

    def pickup_item_by_text_matching(self, text_data, name_set):
        print('Picking item.')
        for idx, text in enumerate(text_data['text']):  # pick first item found
            if text in name_set:
                x, y, w, h = (text_data['left'][idx],
                              text_data['top'][idx],
                              text_data['width'][idx],
                              text_data['height'][idx])
                mid_pt = coord.get_midpoint((x, y), (x + w, y + h))
                print('pick up: ', text, mid_pt)
                self.app.inputs.left_click_on_coords(coords=mid_pt)
                self.action_stack.append(mid_pt)
                self.n_items_picked_up += 1
                time.sleep(self.pickup_delay)
                return True
        return False

    def pickup_items_by_image_matching(self, imgs):
        picked_up = False
        for img in imgs:
            while self.pickup_item_by_image_matching(img):
                picked_up = True
        return picked_up

    def pickup_item_by_image_matching(self, img):
        img_coords = self.find_img_in_screen(img)
        if img_coords:
            print('Picking up item.')
            self.app.inputs.left_click_on_coords(img_coords)
            self.action_stack.append(img_coords)  # reset stack
            time.sleep(self.pickup_delay)
            return True
        return False

    def find_nearest_fog_on_minimap(self):
        self.app.update_screen()
        # cv2.imshow('fog', self.app.get_masked_bgr_minimap('fog'))
        # cv2.waitKey()
        return imgf.nearest_nonzero_idx(self.app.get_masked_bgr_minimap('fog'),
                                        self.minimap_center_pt)

    def go_to_fog(self):  # [105,43,107]
        print('Going to fog.')
        fog_pt = self.find_nearest_fog_on_minimap()
        if fog_pt is not None:
            mini_distance, mini_radians = mv.calc_mini_movement(self.app.get_masked_bgr_minimap('wall'),
                                                                start_pt=self.minimap_center_pt,
                                                                end_pt=fog_pt)
            coords = coord.calc_coords(self.app.screen_center_pt,
                                       self.movement_distance,
                                       mini_radians)
            self.app.inputs.left_click_on_coords(coords)
            self.app.inputs.button_skill('w', coords)
            self.action_stack.append(coords)
            time.sleep(self.movement_delay)
            return True
        return False

    def get_text_data_on_screen_with(self, hsv_color_filter):
        self.app.update_screen()
        item_mask = conv.get_masked_bgr_img(self.app.bgr_screen, hsv_color_filter)
        return txtf.find_text_data(item_mask)

    def open_town_portal(self):
        print('TP needed')
        self.app.inputs.open_inventory()
        time.sleep(.5)
        for img in self.images['inventory']['town_portal']:
            coords = self.find_img_in_screen(img, threshold=.5)
            if coords is not None:
                self.app.inputs.mouse_skill(button='right', coords=coords)
                self.app.inputs.close_all_menus()
                time.sleep(.25)
                return True
        return False

    def go_to_town(self):
        print('Going to town.')
        for img in self.images['objects']['highgate']:
            coords = self.find_img_in_screen(img)
            if coords is not None:
                self.app.inputs.left_click_on_coords(coords)
                self.is_in_town = True
                return True
        return False

    def find_waypoint_box_on_screen(self):
        print('Finding waypoint.')
        self.app.update_screen()
        img_box = imgf.get_template_img_location(self.app.bgr_screen,
                                                 self.images['objects']['waypoint'][0],
                                                 threshold=.6)
        return img_box

    def open_nearby_waypoint_world_menu(self):
        img_box = self.find_waypoint_box_on_screen()
        if img_box is not None:
            print('Opened world menu')
            center_target_img_pt = coord.get_centroid(img_box)
            self.app.inputs.left_click_on_coords((int(center_target_img_pt[0]),
                                                  int(center_target_img_pt[1])))
            self.action_stack.append((int(center_target_img_pt[0]),
                                      int(center_target_img_pt[1])))
            self.n_items_picked_up += 1
            return self.wait_for_world_menu()
        return False

    def create_new_instance_with_world_menu(self, waypoint_menu_btn):
        print('Create new instance.')
        waypoint_menu_coords = self.find_img_in_screen(waypoint_menu_btn)
        if waypoint_menu_coords:
            self.app.inputs.left_click_on_coords(waypoint_menu_coords, pressed='control')
            time.sleep(1.5)
            new_btn_coords = self.find_img_in_screen(self.images['menu_btns']['new_instance_btn'][0])
            if new_btn_coords:
                self.app.inputs.left_click_on_coords(new_btn_coords)
                self.action_stack = list()  # reset stack
                self.is_in_town = False
                return self.wait_for_loading_area()
        return False

    def find_any_pts_on_minimap(self, imgs, threshold=.6):
        self.app.update_screen()
        for img in imgs:
            box_pts = imgf.get_template_img_location(self.app.bgr_minimap, img, threshold)
            if box_pts is not None:
                return box_pts
        return None

    def get_coords_and_distance_in_minimap(self, imgs, threshold=.6):
        box_pts = self.find_any_pts_on_minimap(imgs, threshold)
        if box_pts is not None:  # found target
            center_img_pt = coord.get_centroid(box_pts)
            mini_distance, mini_radians = mv.calc_mini_movement(self.app.get_masked_bgr_minimap('wall'),
                                                                start_pt=self.minimap_center_pt,
                                                                end_pt=center_img_pt)

            coords = coord.calc_coords(self.app.screen_center_pt,
                                       self.movement_distance,
                                       mini_radians)
            return coords, mini_distance
        return None, None

    def get_coords_from_degrees(self, degrees):
        radians = coord.degrees_to_radians(degrees)
        return coord.calc_coords(self.app.screen_center_pt,
                                 self.movement_distance,
                                 radians)

    def go_back_to_waypoint(self, max_moves=25, distance_from_waypoint=50):
        print('Going back to waypoint.')
        n_moves = 0
        while len(self.action_stack) and n_moves < max_moves:
            n_moves += 1
            if self.find_any_pts_on_minimap(self.images['minimap']['waypoint']) is not None:  # backtrack to waypoint
                coords, mini_distance = self.get_coords_and_distance_in_minimap(self.images['minimap']['waypoint'])
                if mini_distance and mini_distance <= distance_from_waypoint:
                    return True
                self.app.inputs.left_click_on_coords(coords)
                self.app.inputs.button_skill('w', coords)
                self.action_stack.append(coords)
                time.sleep(self.movement_delay)
            else:
                prev_coords = self.action_stack.pop()
                inverse_coords = coord.inverse_pts_on_pivot(self.app.screen_center_pt, prev_coords)
                self.app.inputs.left_click_on_coords(inverse_coords)
                self.app.inputs.button_skill('w', inverse_coords)
                time.sleep(self.movement_delay)
        return False

    def explore_one_direction(self,
                              pivot,
                              minimap_pois,
                              direction=None,
                              item_imgs=None,
                              item_name_set=None,
                              distance_from_poi=50,
                              max_moves=25):
        n_moves = 0
        while n_moves < max_moves and self.find_any_pts_on_minimap(pivot) is not None:  # stay near pivot
            n_moves += 1
            coords, mini_distance = self.get_coords_and_distance_in_minimap(minimap_pois)
            if coords and mini_distance:
                if mini_distance <= distance_from_poi:  # we are nearby
                    return True
                self.app.inputs.left_click_on_coords(coords)
                self.app.inputs.button_skill('w', coords)  # move towards POI
                self.action_stack.append(coords)
                time.sleep(self.movement_delay)
                if item_imgs:
                    self.pickup_items_by_image_matching(item_imgs)
                if item_name_set:
                    self.pickup_items_by_text_matching(item_name_set, [0, 255, 254])  # pick up items along the way
            elif not self.go_to_fog():
                return False  # failed to find anything
        return False

    def wait_for_loading_area(self, max_tries=10):
        n_tries = 0
        while not self.find_img_in_screen(self.images['objects']['waypoint'][0]):
            if n_tries >= max_tries:
                return False
            n_tries += 1
            time.sleep(.25)
        return True

    def wait_for_world_menu(self, max_tries=10):
        n_tries = 0
        while not self.find_img_in_screen(self.images['menu_btns']['world'][0]):
            if n_tries >= max_tries:
                return False
            n_tries += 1
            time.sleep(.25)
        return True
