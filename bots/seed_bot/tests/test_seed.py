# self.app.update_screen()
# img_loc = imgf.get_template_img_location(self.app.bgr_minimap, img_to_find, threshold=.6)
# if img_loc is not None:  # found target
#     center_target_img_pt = coord.get_centroid(img_loc)
#     mini_distance, mini_angle = mv.calc_mini_movement(self.app.get_masked_bgr_minimap('wall'),
#                                                       start_pt=self.minimap_center_pt,
#                                                       end_pt=center_target_img_pt)
#     print('angle: ', mini_angle)
#     coords = coord.calc_coords(self.minimap_center_pt, mini_distance, mini_angle)
#     print('coords: ', coords)
#     print(center_target_img_pt)
#     cv2.circle(self.app.bgr_minimap, coords, radius=2, color=(0, 0, 255), thickness=2)
#     # cv2.circle(self.app.bgr_minimap, (int(center_target_img_pt[0]), int(center_target_img_pt[1])), radius=2, color=(0, 255, 0), thickness=2)
#     cv2.imshow('mini', self.app.bgr_minimap)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#
# from bots import seed_bot
#
# s = seed_bot.SeedBot()
# s
