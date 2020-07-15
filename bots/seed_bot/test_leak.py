from poe.bot import poe_bot
import time
import gc

p = poe_bot.POEBot()

n=0
for _ in range(500):
    p.find_img_pt_in_screen(p.images['menu_btns']['quarry'][0])
    time.sleep(.1)
    n += 1
    print(n)