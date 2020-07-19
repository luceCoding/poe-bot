from contextlib import contextmanager


@contextmanager
def waypoint(bot):
    try:
        if not bot.go_to_waypoint():
            raise Warning('Can\'t find waypoint')
        yield
    finally:
        if not bot.go_to_waypoint():
            if not bot.get_out_of_jail():
                raise Warning('Stuck. Help!')

@contextmanager
def world_menu(bot):
    try:
        with waypoint(bot):
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