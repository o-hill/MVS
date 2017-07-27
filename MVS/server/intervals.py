import time
from camera import Camera
import threading
from queue import Queue


# ------------------------------------------------------------------------


class Interval(threading.Thread):
    # This class is a multithreaded component
    # that captures frames from a camera at
    # given intervals.

    def __init__(self, queue):
        # Create a new thread to capture images.
        # INPUTS:
        #    queue: A FIFO queue that is feeding back to the
        #    main thread for image access as this thread is going.
        threading.Thread.__init__(self)
        self.stop = False
        self.streaming = False
        self.queue = queue


    def begin(self, stop_in, interval_in, src = 0):
        # Initialize the starting parameters and let the thread go!
        # stop_in and interval_in are both ints that control the
        # amount of pictures taken in a given time frame.
        self.stop_time = stop_in
        self.interval = interval_in
        self.stream = Camera(src)
        self.source = src # Keep for status messages.
        self.start() # Starts the thread and calls self.run()


    def run(self):
        # Takes images at the given time intervals and
        # puts them in the queue while the time limit has not been reached.
        self.streaming = True
        self.start_time = time.time()
        while time.time() < (self.stop_time + self.start_time) and not self.stop:
            # Put the image in the queue that is feeding back to the main thread.
            self.queue.put(self.stream.get_jpeg())

            # Only take images on the given intervals, so sleep
            # until it's time to run again.
            time.sleep(self.interval - ((time.time() - self.start_time) % self.interval))

        self.streaming = False


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



# ------------------------------------------------------------------------


if __name__ == '__main__':

    q = Queue(maxsize = 0)

    interval = Interval(q)

    total = 6
    lapse = 1


    interval.begin(total, lapse)

    start = time.time()
    i = 0
    while time.time() < start + 6:
        i += 1

    print("i: " + str(i))

    while not q.empty():
        print("one")
        img = q.get()



# ------------------------------------------------------------------------
