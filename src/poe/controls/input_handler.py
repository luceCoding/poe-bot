from random import randrange
from singleton_decorator import singleton

@singleton
class InputHandler():
    def __init__(self, app):
        self._app = app

    def click_on_coords(self,
                        mouse='left',
                        coords=(None, None),
                        pressed=''):  # 'control','shift','alt'
        self._app.send_click(mouse,
                             coords=coords,
                             pressed=pressed)

    def open_inventory(self):
        self._app.move_mouse()  # avoid text hover's blocking inventory
        self._app.send_keystrokes('{SPACE}i')

    def close_all_menus(self):
        self._app.send_keystrokes('{SPACE}')

    def move_mouse(self, coords):
        self._app.move_mouse(coords=coords)

    def mouse_skill(self,
                    button='left',
                    coords=(None, None),
                    pressed=''):
        self._app.send_click(button=button,
                             coords=coords,
                             pressed=pressed)

    def button_skill(self, key, coords=(None, None), variance=None):
        if variance and coords is not None:
            rdm1, rdm2 = randrange(-variance, variance, 25), randrange(-variance, variance, 25)
            new_coords = (map(sum, zip(coords, (rdm1, rdm2))))
            self._app.move_mouse(coords=new_coords)
            self._app.send_keystrokes(key)

    def flask1(self):
        self._app.send_keystrokes('1')

    def flask2(self):
        self._app.send_keystrokes('2')

    def flask3(self):
        self._app.send_keystrokes('3')

    def flask4(self):
        self._app.send_keystrokes('4')

    def flask5(self):
        self._app.send_keystrokes('5')

    # def zoom_map(self):
    #     return  # TODO
    #
    # def zoom_out_map(self):
    #     return  # TODO
