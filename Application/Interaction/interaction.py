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
        self.gathering_box = self.__compute_box_loader()

        self.img_border_resource = cv.imread("images/cropped_bar_resource.png", cv.IMREAD_UNCHANGED)


    def __compute_box_loader(self):
        game_window = self.model.window_capture.get_window_information()

        return 200, 300, 200, 200


    def toggle_ath(self):
        pyautogui.hotkey('alt', 'h')

    def go_on_mount(self):
        pyautogui.press('a')

    def __crop_image_resource(self, img):
        top_x, top_y = 265, 365
        bottom_x, bottom_y = 293, 410

        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)[top_y:bottom_y, top_x:bottom_x]

    def __mining(self, first_image):
        print("Start mining...")

        cuted = self.__crop_image_resource(first_image)

        result = cv.matchTemplate(cuted, self.img_border_resource, cv.TM_CCORR_NORMED)
        _, _, _, max_loc = cv.minMaxLoc(result)

        print(f"Max loc : {max_loc}")
        while max_loc == (0, 1):

            img = self.__crop_image_resource(self.model.window_capture.screenshot())

            result = cv.matchTemplate(img, self.img_border_resource, cv.TM_CCORR_NORMED)
            _, _, _, max_loc = cv.minMaxLoc(result)
            print(f"Mining {max_loc}...")
            sleep(2)

        print("Mining complete")

    def gathering(self, x, y, resource, img):
        self.toggle_ath()
        self.current_gathering = Gathering(x, y, resource)

        pyautogui.leftClick(self.current_gathering.x, self.current_gathering.y, interval=0.5)
        print("Travel to resource...")
        pyautogui.moveTo(10,10)
        sleep(1)
        self.__mining(img)
        self.toggle_ath()

