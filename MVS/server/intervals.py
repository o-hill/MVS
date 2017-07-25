import time
from camera import Camera
import threading

class Interval(threading.Thread):
    # This class is a multithreaded component
    # that captures frames from a camera at
    # given intervals.

    def __init__(self, controller):
        # Create a new thread to capture images.
        # INPUTS:
        #    stop_time: int to specify how long to capture frames for.
        #    interval: int specifying the length of intervals.
        #    controller: a model for saving to the database.
        threading.Thread.__init__(self)
        self.controller = controller
        self.stop = False
        #self.stream = Camera(src)
        #self.stop_time = stop_time_in
        #self.start_time = time.time()
        #self.interval = interval_in
        # self.start()


    def begin(self, stop_in, interval_in, src = 0):
        # Initialize the starting parameters and let the thread go!
        # This class will save the images directly to the database
        # through the LapseController.
        self.stop_time = stop_in
        self.start_time = time.time()
        self.interval = interval_in
        self.stream = Camera(src)
        self.source = src # Keep for status messages.
        self.start()


    def run(self):
        # Takes images at the given time intervals and
        # saves them to the database while the time limit has not been reached.
        self.streaming = True
        while time.time() < (self.stop_time + self.start_time) and not self.stop:
            self.controller.add_image(self.stream.get_jpeg())
            # Save the image as a jpeg.
            # cv2.imwrite("lapse_img_" + str(i) + ".jpg", image)

            # Only take images on the given intervals, so sleep
            # until it's time to run again.
            time.sleep(self.interval - ((time.time() - self.start_time) % self.interval))

        self.streaming = False


    def get_image(self):
        # Needs to return images out of the thread and into the
        # Models module so the image can be saved to the database.
        image = self.stream.get_jpeg()
        return image

    def kill(self):
        self.stop = True


    def is_connected(self):
        # Returns if the camera is able to take images or not.
        img = self.stream.get_jpeg()

        if img is None:
            return False

        return True


    @property
    def status_message(self):
        # Determine what the interval is doing.
        if self.streaming:
            message = "Currently streaming data."
        elif self.is_connected:
            message = "Camera is connected. Not currently streaming."
        else:
            message = "Camera is neither streaming nor connected :("
        return message


    def __del__(self):
        del(self.stream)
