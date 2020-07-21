from src.utils.imaging import img_finder as imgf
from src.utils.math import coordinates as coord
from src.poe.common import movement as mv
from singleton_decorator import singleton
from PIL import Image


@singleton
class MinimapHandler:

    def __init__(self, app, movement_distance):
        self.app = app
        self.movement_distance = movement_distance  # TODO: decouple
        self.minimap_width = self.minimap_height = 275

        self.x1, self.y1 = 1642, 43
        self.x2 = self.x1 + self.minimap_width
        self.y2 = self.y1 + self.minimap_height
        self.mid_x, self.mid_y = self.minimap_width // 2, self.minimap_height // 2
        self.minimap_center_pt = (self.mid_x, self.mid_y)

    # def find_img_in_minimap(self, img_to_find, threshold=.6):
    #     self.app.update_screen()
    #     coords = mini_distance = None
    #     box_pts = imgf.get_template_img_location(self.app.bgr_minimap, img_to_find, threshold)
    #     if box_pts is not None:  # found target
    #         center_img_pt = coord.get_centroid(box_pts)
    #         mini_distance, mini_radians = mv.calc_mini_movement(self.app.get_masked_bgr_minimap('wall'),
    #                                                             start_pt=self.minimap_center_pt,
    #                                                             end_pt=center_img_pt)
    #         coords = coord.calc_coords(self.app.screen_center_pt,  # TODO: decouple
    #                                    self.movement_distance,
    #                                    mini_radians)
    #     return coords, mini_distance

    def find_nearest_fog_on_minimap(self):
        # self.app.update_screen()
        # cv2.imshow('fog', self.app.get_masked_bgr_minimap('fog'))
        # cv2.waitKey()
        masked_bgr_minimap = self.app.get_masked_bgr_minimap('fog')
        idx = imgf.nearest_nonzero_idx(masked_bgr_minimap,
                                       self.minimap_center_pt)
        del masked_bgr_minimap
        return idx

    def find_any_pts_on_minimap(self, imgs, threshold=.6):
        # self.app.update_screen()
        for img in imgs:
            box_pts = imgf.get_template_img_location(self.app.bgr_minimap, img, threshold)
            if box_pts is not None:
                return box_pts
        return None

    def get_coords_and_distance_in_minimap(self, imgs, threshold=.6):
        box_pts = self.find_any_pts_on_minimap(imgs, threshold)
        if box_pts is not None:  # found target
            center_img_pt = coord.get_centroid(box_pts)
            # masked_bgr_minimap = self.app.get_masked_bgr_minimap('wall') # TODO
            mini_distance, mini_radians = mv.calc_mini_movement(self.app.bgr_minimap,
                                                                start_pt=self.minimap_center_pt,
                                                                end_pt=center_img_pt)
            # del masked_bgr_minimap
            coords = coord.calc_coords(self.app.screen_center_pt,  # TODO: decouple
                                       self.movement_distance,
                                       mini_radians)
            return coords, mini_distance
        return None, None

    def get_closest_distance_and_radians_to_minimap_fog(self):
        fog_pt = self.app.minimap_handler.find_nearest_fog_on_minimap()
        if fog_pt is not None:
            masked_bgr_minimap = self.app.get_masked_bgr_minimap('wall')
            mini_distance, mini_radians = mv.calc_mini_movement(masked_bgr_minimap,
                                                                start_pt=self.minimap_center_pt,
                                                                end_pt=fog_pt)
            del masked_bgr_minimap
            return mini_distance, mini_radians
        return None, None

    def crop_minimap(self, img):
        if isinstance(img, Image.Image):
            return img.crop(box=(self.x1, self.y1, self.x2, self.y2))  # rgb
        return img[self.y1:self.y2, self.x1:self.x2]  # bgr numpy

    # def calc_mini_distance_and_radians_from_pt(self, masked_bgr_wall_minimap, end_pt):
    #     distance = abs(coord.calc_distance(self.minimap_center_pt, end_pt))
    #     radians = coord.calc_angle(self.minimap_center_pt, end_pt)
    #     return distance, radians
