# from collections import deque
# import numpy as np
#
# def bfs_non_zero_pixel(bgr_img, x, y):
#     w, h = len(bgr_img), len(bgr_img[0])
#     zeros = np.zeros(3)
#     ones = np.array([255,255,255])
#
#     def get_neighbors(x, y):
#         dirs = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
#         for _x, _y in dirs:
#             _x += x
#             _y += y
#             if 0 <= _x < w and 0 <= _y < h:
#                 if not (bgr_img[_x][_y]==ones).all(): # not visited
#                     yield (_x, _y)
#
#     queue = deque([(x, y)])
#     while queue:
#         x, y = queue.pop()
#         bgr_img[x][y] = ones
#         for _x, _y in get_neighbors(x, y):
#             if not (bgr_img[_x][_y]==zeros).all():
#                 return bgr_img, (_x, _y)
#             queue.appendleft((_x, _y))
#     return None
