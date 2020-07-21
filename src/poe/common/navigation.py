from contextlib import contextmanager
import logging


@contextmanager
def waypoint(bot, movement_delay=None):
    try:
        if not bot.go_to_waypoint(movement_delay=movement_delay):
            raise Warning('Can\'t find waypoint')
        yield
    finally:
        return

@contextmanager
def world_menu(bot, movement_delay=None):
    try:
        with waypoint(bot, movement_delay=movement_delay):
            if not bot.obj_handler.open_object('waypoint'):
                raise Warning('Can\'t open waypoint menu.')
            yield
    finally:
        bot.app.inputs.close_all_menus()

@contextmanager
def inventory(bot):
    try:
        bot.app.inputs.close_all_menus()
        bot.app.inputs.open_inventory()
        yield
    finally:
        bot.app.inputs.close_all_menus()

@contextmanager
def main_rotation(bot):
    try:
        if bot.app.imaging.wait_for_image_on_screen(bot.images['objects']['stash'][0]):
            if bot.move_to_direction(direction_in_degrees=270):
                yield
    finally:
        bot.go_to_character_selection()
        bot.menu_handler.click_on_character_menu_btn('play')
        logging.info('Play character.')