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
        # Return a list of sessions.  SessionController will
        # return a list if neither _id nor data is specified.
        data = SessionController(db)
        return serialize(data.models)


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
        return serialize(session.model)

    def delete(self, session_id):
        # Delete an existing session model.
        session = SessionModel(db, _id = session_id)
        session.delete()

    def put(self, session_id):
        # Camera controls for the session.
        print("id: " + str(session_id))
        data = request.json
        data = deserialize(data)
        for key, value in data.items():
            print("k: " + str(key))
            print("v: " + str(value))
        session = SessionController(db, _id = session_id)
        if data['cmd'] == 'add':
            # Add a camera to the session.
            session.add_camera(data['source'])
        elif data['cmd'] == 'kill':
            # Delete the camera from the session.
            # SHOULD THIS BE DONE WITH THE CAMERA ID INSTEAD? -----------------
            for camera in sessions.cameras:
                if camera.source == data['src']:
                    # If we have found the right camera,
                    # delete it and all images associated with it.
                    camera.delete()

        # Still return the session data, since we want
        # to update the current session in the store.
        return serialize(session.model)



# -----------------------------------------------------------------------------


class Camera(Resource):
    # A single camera object.

    def get(self, camera_id):
        # Get an existing camera model.
        camera = CameraController(db, _id = camera_id)
        return serialize(camera)


    def delete(self, camera_id):
        # Delete an existing target model.
        # ALSO CURRENTLY DELETES ALL IMAGES ASSOCIATED WITH THIS CAMERA.
        camera = CameraController(db, _id = camera_id)
        camera.delete()


    def post(self, camera_id):
        # Creates a target associated with this camera.
        data = request.json
        data = deserialize(data)
        camera = CameraController(db, _id = camera_id)
        camera.add_target(data)


    # PROBABLY WILL ALSO NEED TO CONTROL THE CAMERA HERE.


# -----------------------------------------------------------------------------



class Target(Resource):
    # A single target object.

    def get(self, target_id):
        # Get an existing target model, as well as the images
        # associated with that target.
        target = TargetController(db, _id = target_id)
        images = target.get_lapse()
        return serialize({ 'target': target, 'images': images })


    def delete(self, target_id):
        # Deletes an exisitng target model.
        target = TargetController(db, _id = target_id)
        target.delete()


    #def put(self, target_id):



# ------------------------------------------------------------------------


# Define the api routes.

# Status messages.
api.add_resource(Status, '/status', methods = ['GET'])

# Session creation and listing.
api.add_resource(Sessions, '/sessions', methods = ['GET', 'POST'])

# Read session, add a camera, etc.
allowed_methods = ['GET', 'PUT', 'DELETE']
api.add_resource(Session, '/session/<session_id>', methods = allowed_methods)


# ------------------------------------------------------------------------


if __name__ == '__main__':
    # Launch a server!

    # Production
    # http_server = WSGIServer(('', 1492), app)
    # http_server.serve_forever()

    # Testing/Debugging
    app.run(port = 1492, debug = True, threaded = True)







# ------------------------------------------------------------------------
