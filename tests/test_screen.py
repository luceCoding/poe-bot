import cv2
from src.poe.screen.poe_app import POEApp
import numpy as np

# p = POEApp()
# p.update_screen()
# # p.rgb_minimap.show()
# # cv2.imshow('bgr_mini', p.bgr_minimap)
# # cv2.imshow('fog', p.masked_bgr_minimap('fog'))
# # cv2.imshow('wall', p.masked_bgr_minimap('wall'))
# # cv2.imshow('waypoint', p.masked_bgr_minimap('waypoint'))
# p.rgb_minimap.show()
# m = p.get_masked_bgr_minimap('wall')
# w, h = m.shape[:2]
# mid_x, mid_y = w//2, h//2
# m[mid_x][mid_y] = np.ones(3)*255
# cv2.imshow('wall', m)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

p = POEApp()
p.update_screen()
p.rgb_screen.show()
p.rgb_minimap.show()