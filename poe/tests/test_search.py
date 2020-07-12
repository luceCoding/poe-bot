import cv2
from poe.screen.poeapp import POEApp
from utils.imaging import search
import time
import numpy as np

p = POEApp()
p.update_screen()
m = p.get_masked_bgr_minimap('fog')

zeros = np.zeros(3)
start = time.time()
coords = np.column_stack(np.where(m != zeros))
print(time.time()-start)
print(coords)

print(m[coords[-1][0], coords[-1][1]])

# start = time.time()
# img, pts = search.bfs_non_zero_pixel(m, 50, 50)
# print(pts)
# print(time.time()-start)




# cv2.imshow('search', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
