from abc import abstractmethod
from mss import mss
from numpy import array


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

    def __str__(self):
        return f"Screen located at ({self.left}x, {self.top}y) with size of ({self.width}w, {self.height}h)"


class Capture:
    WINDOWS_NAME = "Albion Online Client"

    def __init__(self, window_name=WINDOWS_NAME):
        self.windowName = window_name

        self.screen = self.__get_screen_information()

        self.grab_coordinates = {
            "top": 0,
            "left": 0,
            "width": 0,
            "height": 0
        }

    def __get_screen_information(self) -> ScreenInformation:
        with mss() as sct:
            info = sct.monitors[1]
            return ScreenInformation(
                top=info["top"],
                left=info["left"],
                width=info["width"],
                height=info["height"]
            )

    @abstractmethod
    def get_window_information(self) -> ScreenInformation | None:
        pass

    @abstractmethod
    def __get_window_id(self) -> int:
        pass

    def screenshot(self) -> array:
        with mss() as sct:
            return array(sct.grab(self.grab_coordinates))

