from .Windows import WindowsCapture
from platform import system
#from .MacOS import MacOSCapture


class CaptureFactory:
    capture = None

    def __init__(self, window_name="Albion Online Client"):

        self.windowName = window_name

        if system() == "Windows":
            self.capture = WindowsCapture(window_name=window_name)
        else:
            pass
            #self.capture = MacOSCapture(window_name=window_name)
