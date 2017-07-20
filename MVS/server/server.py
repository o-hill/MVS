import sys
import numpy as np
from flask import Flask, request, abort
from time import time, sleep
from flask_restful import abort, Api, Resource, reqparse
from flask_cors import *
from gevent.wsgi import WSGIServer
from model import *
from serial import *


# ------------------------------------------------------------------------


# Create a RESTFUL web server
app = Flask(__name__)
api = Api(app)
valid_headers = ['Content-Type', 'Access-Control-Allow-Origin', '*']
cors = CORS(app, allow_headers=valid_headers)

# Connect to the Mongo database.
db = connect_to_database()

# Keep a list of active cameras.
active_cameras = []


# ------------------------------------------------------------------------


class Status(Resource):
    # Get the status of the intervals for a session.
    # Beware: this could potentially return a very large and
    # expensive piece of data, as the list returned is a list of lists,
    # which themselves all contain pairs of strings and booleans.

    def get(self, session_id):
        status_list = []
        session = SessionController(db, _id = session_id)

        for camera in session.cameras:
            # Serialize the data, then put it into the list.
            status_list.append(serialize(camera.get_status()))

        return status_list


# ------------------------------------------------------------------------


class Sessions(Resource):
    # Handles session creation and listing.

    def get(self):
        # Return a list of sessions.


    def post(self):
        # Create a new session model.
        data = request.json
        data = deserialize(data)
        session = SessionController(db, data = data)
        return serialize(session.model)



# ------------------------------------------------------------------------



class Session(Resource):
    # A single session of data recording.

    def get(self, session_id):
        # Get an existing session model.
        session = SessionController(db, _id = session_id)
        return serialize(session)

    def delete(self, session_id):
        # Delete an existing session model.
        session = SessionModel(db, _id = session_id)
        session.delete()

    def put(self, session_id):
        # Takes commands to allocate another camera to the session.
        data = request.json
        data = deserialize(data)
        session = SessionController(db, _id = session_id)
        session.add_camera(data['source'])






# ------------------------------------------------------------------------



class Camera(Resource):
    # A single timelapse object.

    def get(self, camera_id):
        # Get an existing lapse model.
        camera = CameraController(db, _id = camera_id)
        return serialize(camera)

    def delete(self, camera_id):
        # Delete an existing target model.
        camera = CameraController(db, _id = camera_id)
        camera.delete()


    def put(self, camera_id):
        # Controls the function of a target.







# ------------------------------------------------------------------------
