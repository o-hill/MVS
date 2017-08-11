# Written by Oliver Hill <oliverhi@umich.edu>
# For Michigan Aerospace Corporation, for the MVS Microscope project.


import time
from scheduler import Scheduler
from model import *
from motor import CameraMotor


class MasterCamera():


    def __init__(self, database):
        self.controller = {}
        self.db = database
        self.scheduler = Scheduler(self)
        self.location = {
            'x': 0,
            'y': 0,
            'z': 0
        }
        self.motor = CameraMotor(self.location)


    def get_location(self, target_id):
        # Get the location of a target, given the id.
        target = TargetController(self.db, _id = target_id)
        return target.model['cords']


    def move(self, location):
        # Move the camera motors and update the location.
        self.motor.move(location)
        self.current = self.motor.get_location()


    def add_target(self, target):
        # Add a target to the motor schedule.
        # The target.schedule must already be formatted correctly.
        self.scheduler.add_target(target.schedule)






# -----------------------------------------------------------------------------
