import pywinauto
from pywinauto.application import Application
import win32gui
import ctypes

class App:
    def __init__(self, title, index=0):
        self._app = Application().connect(title=title, found_index=index)
        self._app_window = self._app[title]
        self._rect = pywinauto.win32structures.RECT()
        self._hwin = self._app.top_window()
        self._window_title = self._hwin.window_text()
        self._DWMWA_EXTENDED_FRAME_BOUNDS = 9
        self._byref_rect = ctypes.byref(self._rect)
        self._sizeof_rect = ctypes.sizeof(self._rect)

    def get_screen_as_rgb_img(self):
        self._hwin.set_focus()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            ctypes.wintypes.HWND(win32gui.FindWindow(None, self._window_title)),
            ctypes.wintypes.DWORD(self._DWMWA_EXTENDED_FRAME_BOUNDS),
            self._byref_rect,
            self._sizeof_rect
        )
        return self._hwin.capture_as_image(self._rect)

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