import cv2 as cv
import numpy as np
from time import time,sleep
from capture import WindowCapture
from vision import Vision
from gui import GUI
from datetime import datetime
import keyboard
def saveImg(name:str, img:np.ndarray):
    path = f"output/{name}.jpg"
    cv.imwrite(path, img)

def drawRectangle():
    default_image = cv.imread('../ressources/stone.png', cv.IMREAD_REDUCED_COLOR_2)
    looking_for = cv.imread('../ressources/stone-alone.png', cv.IMREAD_REDUCED_COLOR_2)

    formats = [cv.TM_SQDIFF,cv.TM_CCOEFF, cv.TM_CCORR_NORMED,cv.TM_CCORR,cv.TM_CCOEFF_NORMED]

    result = cv.matchTemplate(default_image, looking_for, formats[4])

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    print(max_val, max_loc)

    if max_val >= 0.8:
        print("Founded values")

        looking_w = looking_for.shape[1]
        looking_h = looking_for.shape[0]

        top_left = max_loc
        bottom_right = (top_left[0] + looking_w, top_left[1] + looking_h)

        cv.rectangle(default_image, max_loc, bottom_right, color=(255, 0, 0), thickness=2, lineType=cv.LINE_4)

        saveImg("founded-stone", default_image)

    else:
        print("Nothing founded")

def showImageUntilKeyPressed(image):
    cv.imshow("Result", image)
    cv.waitKey()


def findMultipleImages():

    positions = []

    default_image = cv.imread('../ressources/stone.png', cv.IMREAD_UNCHANGED)
    looking_for = cv.imread('../ressources/stone-alone.png', cv.IMREAD_UNCHANGED)

    formats = [cv.TM_SQDIFF,cv.TM_CCOEFF, cv.TM_CCORR_NORMED,cv.TM_CCORR,cv.TM_CCOEFF_NORMED]

    result = cv.matchTemplate(default_image, looking_for, formats[4])

    looking_w = looking_for.shape[1]
    looking_h = looking_for.shape[0]

    threshold = 0.53
    locations = np.where(result >= threshold)

    locations = list(zip(*locations[::-1]))

    rectangles = []

    for location in locations:
        rect = [int(location[0]),int(location[1]),looking_w,looking_h]

        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

    for (x,y,w,h) in rectangles:

        top_left = (x,y)
        bottom_right = (x + w, y + h)

        center_x = x + int(w/2)
        center_y = y + int(h/2)

        positions.append((center_x,center_y))

        cv.drawMarker(default_image,(center_x,center_y), (0,0,255), thickness=1)
        #cv.rectangle(default_image, top_left, bottom_right, color=(255, 0, 0), thickness=2, lineType=cv.LINE_4)

    saveImg("founded-stones",default_image)
    showImageUntilKeyPressed(default_image)

    return positions

def realTimeCapture():

    sleep(3)

    GUI()

    loop_time = time()

    windowCapture = WindowCapture()

    looking_for = cv.imread('../ressources/stone-island.png', cv.IMREAD_UNCHANGED)

    looking_for = cv.cvtColor(looking_for,cv.COLOR_RGB2BGR)
    while True:

        screenshot = windowCapture.screenshot()

        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        Vision.click_in_middle(screenshot,looking_for)

        break
        if keyboard.is_pressed(0XFF):
            cv.imshow()
            cv.destroyAllWindows()
            break

    print("Done")


def getImageFromGamePressingF():

        sleep(3)
        screenshot = None
        windowCapture = WindowCapture()

        while True:

            screenshot = windowCapture.screenshot()

            key = cv.waitKey(1)
            print(key)

            if key == ord('q'):
                cv.destroyAllWindows()
                date = datetime.now().strftime("%H_%M_%S")
                WindowCapture.save_image(f"output/dataset/screenshot_{date}.png", screenshot)
                break

        print("Done")


def main():

    GUI()

    #getImageFromGamePressingF()

    #realTimeCapture()

    """
    for format in formats:
        result = cv.matchTemplate(default_image, looking_for,format)
        cv.imshow("Matched Image",result)
        cv.waitKey()
    """
if __name__ == "__main__":
    main()