from src.poe.bot.poe_bot import POEBot

# p = POEApp()
# m = MenuNavigator(p)

# btns = ['part1', 'part2', 'epi']
# btns2 = ['part2', '6', '7', '8', '9', '10']
#
# for btn in btns:
#     m.click_on_menu_btn(btn)
#     time.sleep(1)
#
# for btn in btns2:
#     m.click_on_menu_btn(btn)
#     time.sleep(1)

# objs = ['stash', 'seed_stockpile', 'waypoint']
# for obj in objs:
#     print(obj, m.open_object(obj))
#     p.inputs.close_all_menus()
#     time.sleep(1)

p = POEBot()
p.app.inputs.mouse_skill(button='right')  # cast righteous fire
# p.n_items_picked_up = 300
# p.open_nearby_waypoint_world_menu()
# p.menu_handler.drop_off_all_inventory()

print(p.open_nearby_waypoint_world_menu(drop_off=True,
                                        drop_order=['seed_stockpile', 'stash']))