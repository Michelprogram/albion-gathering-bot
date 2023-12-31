from time import sleep
from Albion.detection import AlbionDetection
from Application.Interaction.interaction import Interaction
from Capture import Windows
import cv2 as cv


def run():
    sleep(2)
    model = AlbionDetection(debug=True, confidence=0.8)
    while True:
        model.predict()

        if model.debug:

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break


def gathering():
    sleep(2)
    model = AlbionDetection(debug=False, confidence=0.8)
    interaction = Interaction(model)

    x, y, resource, img = model.predict()

    interaction.gathering(x, y, resource, img)
    while True:

        if model.debug:

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break


def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # draw circle here (etc...)
        print('x = %d, y = %d' % (x, y))


def crop_border_resource():
    img = cv.imread("640x640_resource.png", cv.IMREAD_GRAYSCALE)

    top_x, top_y = 265, 366
    bottom_x, bottom_y = 293, 372

    cuted = img[top_y:bottom_y, top_x:bottom_x]

    cv.imwrite("images/cropped_bar_resource.png", cuted)


def crop_image():
    img = cv.imread("640x640_no_resource.png", cv.IMREAD_GRAYSCALE)
    border = cv.imread("images/cropped_bar_resource.png", cv.IMREAD_UNCHANGED)

    top_x, top_y = 265, 365
    bottom_x, bottom_y = 293, 410

    cuted = img[top_y:bottom_y, top_x:bottom_x]

    result = cv.matchTemplate(cuted, border, cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    print('Best match top left position: %s' % str(max_loc))
    print('Best match confidence: %s' % max_val)

    # Get the size of the needle image. With OpenCV images, you can get the dimensions
    # via the shape property. It returns a tuple of the number of rows, columns, and
    # channels (if the image is color):
    needle_w = border.shape[1]
    needle_h = border.shape[0]

    # Calculate the bottom right corner of the rectangle to draw
    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    # Draw a rectangle on our screenshot to highlight where we found the needle.
    # The line color can be set as an RGB tuple
    cv.rectangle(cuted, top_left, bottom_right,
                 color=(0, 255, 0), thickness=1, lineType=cv.LINE_4)

    # You can view the processed screenshot like this:
    # cv.imshow('Result', haystack_img)
    # cv.waitKey()
    # Or you can save the results to a file.
    # imwrite() will smartly format our output image based on the extension we give it
    # https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce
    cv.imwrite('result_2.jpg', cuted)

    cv.imwrite("cropped.png", cuted)

    cv.imshow("Test", cuted)
    cv.waitKey(0)


def read_cropped_image():
    model = AlbionDetection(debug=False, confidence=0.8)

    border = cv.imread("images/cropped_bar_resource.png", cv.IMREAD_UNCHANGED)

    top_x, top_y = 265, 365
    bottom_x, bottom_y = 293, 410

    i = 0

    while True:
        cuted = model._process_image(model.window_capture.screenshot())[top_y:bottom_y, top_x:bottom_x]

        cuted = cv.cvtColor(cuted, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(cuted, border, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        print('Best match top left position: %s' % str(max_loc))
        print('Best match confidence: %s' % max_val)

        needle_w = border.shape[1]
        needle_h = border.shape[0]

        # Calculate the bottom right corner of the rectangle to draw
        top_left = max_loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

        # Draw a rectangle on our screenshot to highlight where we found the needle.
        # The line color can be set as an RGB tuple
        cv.rectangle(cuted, top_left, bottom_right,
                     color=(0, 255, 0), thickness=1, lineType=cv.LINE_4)

        cv.imwrite(f'images/data/test-{i}.png', cuted)
        i += 1
        sleep(2)


def testWindowsCapture():
    window = Windows.WindowsCapture()
    img = window.screenshot()

    cv.imshow("Founded", img)
    cv.waitKey(0)


if __name__ == "__main__":
    #read_cropped_image()
    gathering()
    # crop_image()
    # crop_border_resource()
