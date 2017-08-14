# Written by Oliver Hill <oliverhi@umich.edu>
# For Michigan Aerospace Corporation, for the MVS Microscope project.

import time
import threading

class Scheduler(threading.Thread):
    # A threaded component to maintain the motor
    # scheduling for capturing images.

    def __init__(self, master):
        self.schedule = []
        self.master = master
        self.wait = False
        self.restart = True
        self.first = True


    def run(self):
        self.stop = False

        while self.restart:
            self.restart = False
            for item in self.schedule:

                while self.wait:
                    # Do nothing... Wait for auto mode.
                    if self.restart:
                        # If a location gets added, restart the loop.
                        break
                if self.restart:
                    break

                # Get the coordinates from the id of the next target.
                destination = self.master.get_location(item[1])
                # Move to the destination.
                self.master.move(destination)
                self.current = self.motor.get_location()

                while time.time() < (item[0] + 1):
                    # While the current time is less than the time that
                    # the image will be taken plus one second, wait
                    # and potentially get more instructions.
                    if self.restart:
                        # If a location gets added, restart the loop.
                        break
                if self.restart:
                    break


    def add_location(self, location):
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

        self.restart = True

        if self.first:
            # Start the schedule.
            self.start()


    def manual(self):
        self.wait = True


    def auto(self):
        self.wait = False




# -----------------------------------------------------------------------------
