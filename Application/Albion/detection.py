import cv2 as cv
import torch
from Application.Capture.Factory import CaptureFactory
from time import time
from math import sqrt


class AlbionDetection:
    MODEL_NAME = "best.pt"
    IMG_SIZE = 640
    CONFIDENCE = 0.5

    def __init__(self,
                 model_name=MODEL_NAME,
                 debug=False,
                 confidence=CONFIDENCE,
                 window_name="Albion Online Client"
                 ):
        """
        Initialize the AlbionDetection object.

        :param model_name: Name of the YOLOv5 model file.
        :param debug: Flag to enable debug mode.
        """
        self.model_name = model_name
        self.model = self._load_model()
        self.classes = self._load_classes()
        self.window_capture = CaptureFactory(window_name).capture
        self.debug = debug
        self.confidence = confidence
        self.character_position_X = self.IMG_SIZE / 2
        self.character_position_Y = self.IMG_SIZE / 2 - 60

    def _process_image(self, img):
        """
        Preprocess the image.

        :param img: Input image.
        :return: Processed image.
        """
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        return cv.resize(img, (self.IMG_SIZE, self.IMG_SIZE))

    def _load_classes(self):
        """
        Load class information.

        :return: Dictionary containing class information.
        """
        classes = {}
        for k, v in self.model.names.items():
            classes[k] = {
                "label": v,
                "color": (0, 255, k * 10)
            }
        return classes

    def draw_boxes(self, img, coordinates):
        """
        Draw bounding boxes on the image.

        :param img: Input image.
        :param coordinates: Bounding box coordinates.
        """
        for coord in coordinates:
            x1, y1, x2, y2 = coord[:4].int()
            confidence, class_id = coord[4], self.classes[int(coord[5])]
            cv.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), class_id["color"], 2)
            label = f"{class_id['label']} {confidence:.2f}"
            cv.putText(img, label, (int(x1), int(y1) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, class_id["color"], 2)

        self.__cross_line(img)

        cv.drawMarker(img, (int(self.character_position_X), int(self.character_position_Y)), (255, 255, 255),
                      cv.MARKER_DIAMOND, 10, 2)
        self.__marker_closest(img, coordinates)
        # cv.imshow("Boxes", img)

    def __cross_line(self, img):
        cv.line(img, (0, int(self.character_position_X)), (self.IMG_SIZE, int(self.character_position_X)),
                (255, 255, 255), 2)
        cv.line(img, (int(self.character_position_X), 0), (int(self.character_position_X), self.IMG_SIZE),
                (255, 255, 255), 2)

    def __marker_closest(self, img, coordinates):
        closest = self.closest_point(coordinates)

        if closest is not None:
            cv.drawMarker(img, (int(closest[0]), int(closest[1])), (37, 150, 190), cv.MARKER_CROSS, 10, 2)
            cv.putText(img, "Closest", (int(closest[0]), int(closest[1]) + 50), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                       (0, 255, 0), 2)

    def closest_point(self, coordinates):

        if len(coordinates) == 0:
            return None

        min = self.IMG_SIZE
        position = 0

        centers = []

        for index, coord in enumerate(coordinates):
            x1, y1, x2, y2 = coord[:4].int()

            center_x, center_y = ((x2 - x1) / 2) + x1, ((y2 - y1) / 2) + y1

            computed = sqrt(
                abs(self.character_position_X - center_x) ** 2 + abs(self.character_position_Y - center_y) ** 2)

            if computed < min:
                min = computed
                position = index

            centers.append((center_x, center_y, coord[5].int()))

        return centers[position]

    def __convert_coordinates_to_screen_position(self, center_x, center_y):

        center_x = ((center_x * self.window_capture.window.width) / self.IMG_SIZE) + self.window_capture.window.left
        center_y = ((center_y * self.window_capture.window.height) / self.IMG_SIZE) + self.window_capture.window.top
        return center_x, center_y

    def _load_model(self):
        """
        Load the YOLOv5 model.

        :return: Loaded YOLOv5 model.
        """
        try:
            model = torch.hub.load('yolov5', 'custom', path=self.MODEL_NAME, source="local", force_reload=True,
                                   verbose=True)

        except Exception as e:
            raise Exception(f"Failed to load the model: {e}")

        return model

    def predict(self):
        """
        Make predictions using the YOLOv5 model.
        """
        loop_time = time()
        img = self._process_image(self.window_capture.screenshot())
        res = self.model(img)
        coordinates = [coord for coord in res.xyxy[0] if coord[4].item() > self.confidence]

        if self.debug:
            self.draw_boxes(img, coordinates)
            cv.putText(img, f'FPS {1 / (time() - loop_time)}', (10, 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                       1)
            cv.imshow("Founded", img)
            loop_time = time()

        center_x, center_y, ressource = self.closest_point(coordinates)

        center_x, center_y = self.__convert_coordinates_to_screen_position(center_x, center_y)

        return center_x, center_y, ressource, img
