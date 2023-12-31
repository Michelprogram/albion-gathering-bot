from Application.Albion.detection import AlbionDetection
from time import sleep
import cv2 as cv
import pyautogui


class Gathering:
    def __init__(self, x, y, resource):
        self.x = x
        self.y = y
        self.resource = resource


class Interaction:

    def __init__(self, model):
        self.model: AlbionDetection = model
        self.current_gathering: Gathering | None = None

        self.debug = self.model.debug
        self.img_border_resource = cv.imread("images/cropped_bar_resource.png", cv.IMREAD_UNCHANGED)


    def toggle_ath(self):
        pyautogui.hotkey('alt', 'h')

    def go_on_mount(self):
        pyautogui.press('a')

    def __crop_image_resource(self):
        top_x, top_y = 265, 365
        bottom_x, bottom_y = 293, 410

        img = self.model._process_image(self.model.window_capture.screenshot())

        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)[top_y:bottom_y, top_x:bottom_x]

    def __is_mining(self):
        img = self.__crop_image_resource()

        result = cv.matchTemplate(img, self.img_border_resource, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(result)

        if self.debug:
            print(max_val)

        return max_val >= 0.8

    def __mining(self):
        if self.debug:
            print("Start Minning...")

        while self.__is_mining() is True:
            sleep(2)
            pass

        print(self.__is_mining())

        if self.debug:
            print("Minning completed")

    def __moving(self):

        if self.debug:
            print("Start mooving...")

        while self.__is_mining() is False:
            pass

        if self.debug:
            print("Mooving completed")

    def gathering(self, x, y, resource):
        self.toggle_ath()
        self.current_gathering = Gathering(x, y, resource)

        pyautogui.leftClick(self.current_gathering.x, self.current_gathering.y, interval=0.5)
        pyautogui.moveTo(10, 10)

        self.__moving()
        self.__mining()

        self.toggle_ath()

