# Written by Oliver Hill <oliverhi@umich.edu>
# For Michigan Aerospace Corporation, for the MVS Microscope project.


import time
from scheduler import Scheduler
from model import *


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

    def get_location(self, target_id):
        # Get the location of a target, given the id.
        target = TargetController(self.db, _id = target_id)
        return target.model['cords']
