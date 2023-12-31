from mss import mss
from . import Capture, ScreenInformation
import Quartz
import numpy as np


class MacOSCapture(Capture):

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
