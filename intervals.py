import time
from camera import Camera
import cv2
import threading

class Interval(threading.Thread):
    # This class is a multithreaded component
    # that captures frames from a camera at
    # given intervals.

    def __init__(self, stop_time_in, interval_in, src = 0):
        # Create a new thread to capture images.
        # INPUTS:
        #    stop_time: int to specify how long to capture frames for.
        #    interval: int specifying the length of intervals.
        #    src: int to indicate which port to read frames from.

        threading.Thread.__init__(self)
        self.stream = Camera(src)
        self.stop_time = stop_time_in
        self.start_time = time.time()
        self.interval = interval_in
        self.start()

    def run(self):
        # Takes images at the given time intervals and
        # saves them to the disk while the time limit has not been reached.
        i = 0
        while time.time() < (self.stop_time + self.start_time):
            image = self.stream.get_jpeg()
            # Save the image as a jpeg.
            cv2.imwrite("lapse_img_" + str(i) + ".jpg", image)
            i += 1

            # Only take images on the given intervals, so sleep
            # until it's time to run again.
            time.sleep(self.interval - ((time.time() - self.start_time) % self.interval))


    def __del__(self):
        del(self.stream)
