import sys
import numpy as np
from flask import Flask, request, abort
from time import time, sleep
from flask_restful import abort, Api, Resource, reqparse
from flask_cors import *
from gevent.wsgi import WSGIServer


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
    # Get the status of the intervals.

    def get(self):
        status_list = []

        for camera in active_cameras:
            data = {}
            data['is_connected'] = camera.is_connected
            data['status'] = camera.status_message
            data['source'] = camera.source
            # Serialize the data, then put it into the list.
            status_list.append(serialize(data))

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

    # def put(self, session_id):
    #     # Takes commands to start or stop intervals.
    #     data = request.json
    #     data = deserialize(data)
    #     session = SessionController(db, _id = session_id)
    #     command = data['cmd']
    #     if command == 'start':
    #         # Data must include start time, stop time, interval, and source.
    #



# ------------------------------------------------------------------------



class Timelapse(Resource):
    # A single timelapse object.

    def get(self, lapse_id):
        # Get an existing lapse model.
        lapse =
