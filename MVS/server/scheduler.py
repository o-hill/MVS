# Written by Oliver Hill <oliverhi@umich.edu>
# For Michigan Aerospace Corporation, for the MVS Microscope project.

import time
from motor import CameraMotor
import threading



class Scheduler(threading.Thread):

    def __init__(self, master):
        self.schedule = []
        self.motor = CameraMotor(master.location)
        self.master = master
        self.current = self.motor.get_location()
        self.stop = False


    def run(self):
        self.stop = False
        # Begin at the initial location.
        destination = self.master.get_location(self.schedule[0][1])
        self.current = self.motor.move(destination)

        for item in self.schedule:

            while time.time() < (item[0] + 1):
                # While the current time is less than the time that
                # the image will be taken plus one second, wait
                # and potentially get more instructions.
                if self.stop:
                    # If locations are being added, break
                    # out of the thread.
                    break

            if self.stop:
                break

            # Get the coordinates from the id of the next target.
            destination = self.master.get_location(item[1])
            # Move to the destination.
            self.motor.move(destination)
            self.current = self.motor.get_location()
            # Wait for instructions until




    def add_location(self, location):
        # First, stop the thread if it is active.
        self.stop = True

        # Add the times for a new location to the schedule,
        # adding a "Image Captured" attribute.
        # PRE-REQUISITE STRUCTURE:
        #   ( <TIME TO TAKE IMAGE>, <TARGET ID> ).
        for item in location:
            self.schedule += (item[0], item[1], False)

        # Iterate over a copy of the schedule,
        # and remove any times from the schedule which have already passed.
        for item in list(self.schedule):
            if item[0] < time.time():
                self.schedule.remove(item)

        # Finally, sort the list by time, leaving us with
        # a schedule of locations to visit.
        self.schedule = sorted(self.schedule, lambda x: x[0])

        # Start the schedule.
        self.start()


    def get_location(self):
        return self.current









# -----------------------------------------------------------------------------
