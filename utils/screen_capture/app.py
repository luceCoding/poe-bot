from pywinauto.application import Application

class App:
    def __init__(self, title, index=0):
        self._app = Application().connect(title=title, found_index=index)
        self._app_window = self._app[title]

    def get_screen_as_rgb_img(self):
        self._app_window.set_focus()
        return self._app_window.capture_as_image()

    def send_keystrokes(self, keys):
        self._app_window.send_keystrokes(keys)

    def send_click(self, button, coords=(None,None), pressed='', double=False):
        self._app_window.click_input(button,
                                     coords=coords,
                                     pressed=pressed,
                                     double=double)

    def move_mouse(self, coords=(None,None)):
        self._app_window.click_input('move',
                                     coords=coords)