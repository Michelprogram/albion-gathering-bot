import cv2 as cv
import numpy as np

class Vision:

    @staticmethod
    def click_in_middle(current_image, looking_for):
        positions = []

        result = cv.matchTemplate(current_image, looking_for, cv.TM_CCOEFF_NORMED)

        looking_w = looking_for.shape[1]
        looking_h = looking_for.shape[0]

        threshold = 0.60
        locations = np.where(result >= threshold)

        locations = list(zip(*locations[::-1]))

        rectangles = []

        for location in locations:
            rect = [int(location[0]), int(location[1]), looking_w, looking_h]

            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

        for (x, y, w, h) in rectangles:

            center_x = x + int(w / 2)
            center_y = y + int(h / 2)

            positions.append((center_x, center_y))

            cv.drawMarker(current_image, (center_x, center_y), (0, 0, 255), thickness=1)
            # cv.rectangle(default_image, top_left, bottom_right, color=(255, 0, 0), thickness=2, lineType=cv.LINE_4)

        cv.imwrite("output/test-2.png", current_image)

        return positions
    