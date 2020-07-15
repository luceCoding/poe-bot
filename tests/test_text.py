from src.utils import App
from src import utils as con

screen = App(title='Path of Exile')
rgb_screen = screen.get_app_rgb_img()

# starttime = timeit.default_timer()
bgr_screen = con.rgb_to_bgr(rgb_screen)
#masked_img = con.get_masked_img(bgr_screen, [152, 255, 200]) # pink seeds
masked_img = con.get_masked_bgr_img(bgr_screen, [119, 73, 192]) # walls
#masked_img = con.get_masked_img(bgr_screen, [99, 226, 191]) # fog
#masked_img = con.get_masked_img(bgr_screen, [111, 10, 255]) # waypoint
# print(timeit.default_timer() - starttime)
#print(tx.find_text_locations(bgr_screen))

# found_txt = tx.find_text_strings(masked_img).split('\n')
# pprint(list(filter(None, found_txt)))
#
# d = tx.find_text_data(masked_img)
# n_boxes = len(d['level'])
# for i in range(n_boxes):
#     (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#     cv2.rectangle(bgr_screen, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# cv2.imshow('img', bgr_screen)
# cv2.imshow('masked', masked_img)
# cv2.waitKey(0)