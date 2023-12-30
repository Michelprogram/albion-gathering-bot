import numpy as np
from mss import mss
import Quartz


class ScreenInformation:

    top = 0
    left = 0
    width = 0
    height = 0

    ALBION_HEADER_HEIGHT = 30

    def __init__(self, top, left, width, height):
        self.top = top + self.ALBION_HEADER_HEIGHT
        self.left = left
        self.width = width
        self.height = height - self.ALBION_HEADER_HEIGHT

    def center(self):
        return (self.width + self.top) / 2, (self.height + self.left) / 2


class WindowCapture:

    def __init__(self, window_name="Albion Online Client"):
        self.windowName = window_name
        self.hwnd = self.__get_window_id()

        self.window = self.__get_window_information()
        self.screen = self.__get_screen_information()

        self.grab_coordinates = {
            "top": self.window.top,
            "left": self.window.left,
            "width": self.window.width,
            "height": self.window.height
        }

    def __get_screen_information(self):
        with mss() as sct:
            info = sct.monitors[1]
            return ScreenInformation(
                top=info["top"],
                left=info["left"],
                width=info["width"],
                height=info["height"]
            )

    def __get_window_information(self):
        window_info_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionIncludingWindow, self.hwnd)

        for window_info in window_info_list:
            window_id = window_info[Quartz.kCGWindowNumber]
            if window_id == self.hwnd:
                bounds = window_info[Quartz.kCGWindowBounds]
                return ScreenInformation(
                    top=bounds['Y'],
                    left=bounds['X'],
                    width=bounds['Width'],
                    height=bounds['Height']
                )
        return None

    def __get_window_id(self):
        windowList = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)

        for window in windowList:
            if self.windowName.lower() in window.get('kCGWindowName', '').lower():
                hwnd = window['kCGWindowNumber']
                return hwnd

        raise Exception('could not find window named %s' % self.windowName)


    def screenshot(self):
        with mss() as sct:
            return np.array(sct.grab(self.grab_coordinates))