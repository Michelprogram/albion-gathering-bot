from abc import ABC

import win32gui

from . import Capture, ScreenInformation


class WindowsCapture(Capture, ABC):

    def __init__(self, window_name=Capture.WINDOWS_NAME):
        super().__init__(window_name)

        self.hwnd = self.__get_window_id()
        self.window = self.get_window_information()

        self.grab_coordinates = {
            "top": self.window.top,
            "left": self.window.left,
            "width": self.window.width,
            "height": self.window.height
        }

    def get_window_information(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        return ScreenInformation(
            top=rect[1],
            left=rect[0],
            width=rect[2] - rect[0],
            height=rect[3] - rect[1]
        )

    def __get_window_id(self):
        hwnd = win32gui.FindWindow(None, self.windowName)

        if hwnd == 0:
            raise Exception('could not find window named %s' % self.windowName)

        return hwnd

