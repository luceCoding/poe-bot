from contextlib import contextmanager


@contextmanager
def waypoint(bot, movement_delay=None):
    try:
        if not bot.go_to_waypoint(movement_delay=movement_delay):
            raise Warning('Can\'t find waypoint')
        yield
    finally:
        return
        # if not bot.go_to_waypoint():
        #     if not bot.get_out_of_jail():
        #         raise Warning('Stuck. Help!')

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