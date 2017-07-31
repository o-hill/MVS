from pymongo import MongoClient
from database import *
import logging as log
from bson import ObjectId
import time
import cv2
from intervals import Interval
from queue import Queue
#from motor import CameraMotor

# For converting the 2D image array into Mongo-friendly format
from bson import Binary
import pickle


# --------------------------------------------------------------------------


class ModelController(object):
    # Base class for dealing with models and saving to databases.


    def __init__(self, model_name, database, data = None, _id = None):
        # Connect to a database.  Load or create the model.
        self.db = database
        self.model_name = model_name
        self.collection = self.db[model_name]

        # Logging?
        #log.basicConfig(level = verbose)
        #self.log = log.getLogger(__name__)

        if (data is None) and (_id is None):
            # If nothing is specified, load all session models.
            self._list()

        if (data is not None):
            # Default is to create a new session.
            data['created_at'] = created_at()
            self.create(data)

        if (_id is not None):
            # Attempt to look up the session given the id.
            if (type(_id) is str): # Convert to ObjectID format.
                _id = ObjectId(_id)
            self._id = _id
            self.read()


    def _read(self):
        # Find a specific model given its id.
        self.model = self.collection.find_one(qwrap(_id))


    def _list(self):
        # Delete the current resource.
        self.models = list(self.collection.find())
        return self.models


    def _delete(self):
        # Delete the current resource.
        self.colection.delete_one(qwrap(self._id))


    def _create(self, data):
        # Create a new model in the database.  Call this for core update.
        if self.validate(data):
            #self.log.info('> Attempting to create a new model in {:s}'.\
                #format(self.model_name))

            try:
                insertion = self.collection.insert_one(data)
            except:
                print("Didn't insert correctly!")
                return
                #self.log.exception('> Critical error in creating {:s}.'.\
                    #format(self.model_name))

            #self.log.info('> Created a new model in {:s}'.format(self.model_name))
            self.model = find_inserted_document(insertion, self.collection)
            self._id = self.model['_id']
            return self.model


    def create(self, data):
        # Override as necessary.
        session = self._create(data)


    def validate(self, data):
        # Ensure the proposed object has required fields.
        for attribute in self.required_attributes:
            if attribute not in data:
                raise ValueError('Field "{:s}" is not present in the data.'.\
                    format(attribute))
        return True


    def _update(self):
        # Saves the current model to the database.
        #self.log.info(' > Updating current model in {:s}'.format(self.\
                #model_name))
        self.collection.update_one(qry(self.model), { '$set': self.model })


    def _read(self):
        # Retrieve the core model from the database.
        self.model = self.collection.find_one(qwrap(self._id))
        self._id = self.model['_id']


    def _delete(self):
        # Delete the core model from the database.
        self.collection.delete_one(qwrap(self._id))


    @property
    def required_attributes(self):
        return []



# --------------------------------------------------------------------------



class SessionController(ModelController):
    # Handle session creation, updating, etc.
    # A session is a single recording session on one or multiple cameras.

    def __init__(self, database, data = None, _id = None):
        # Initialize the model as a sessions object.
        ModelController.__init__(self, 'sessions', database, data=data, _id=_id)
        #self.model['cameras'] = []


    def read(self):
        # Read a specific session from the database.
        self._read()
        # if self.model:
        #     self.load_series()
        #     self.load_annotations()


    def add_camera(self, source):
        camera_data = {}
        camera_data['owner_id'] = self._id
        camera = CameraController(self.db, source, data = camera_data)
        self.model['cameras'].append(camera._id)
        self._update()
        return camera


    def load_annotations(self):
        # Load all annotations.
        query = {}
        query['owner_id'] = self._id
        self.annotations = list(self.db.annotations.find(query))
        self.model['annotations'] = self.annotations


    def delete(self):
        # Delete the current session and all associated cameras.
        for camera in self.cameras:
            camera.delete()

        self._delete()

    def get_cameras(self):
        query = {}
        query['owner_id'] = self._id
        return list(self.db.camera.find(query))


# --------------------------------------------------------------------------



class CameraController(ModelController):
    # Deals with an individual camera in the system.

    def __init__(self, database, source, data = None, _id = None):
        # Initialize as a camera object.
        ModelController.__init__(self, 'camera', database, data=data, _id=_id)
        # A source number must be specified.
        self.model['source'] = source
        # Blank list of targets belonging to the camera.
        self.model['targets'] = []
        self.model['num_targets'] = 0
        # Start the camera in the center of the dish.
        #self.motor = CameraMotor(0, 0, 0)
        #self.current = self.motor.get_location()
        self._update()

    def read(self):
        # Read the current camera from the database.
        self._read()


    def add_target(self, data):
        # Required data points:
        #   cords: a dictionary containing:
        #       x, y, and z for positioning camera
        #   Total amount of time to take images for.
        #   Interval time.
        target_data = {}
        target_data['cords'] = data['cords']
        target_data['source'] = self.source
        target_data['time'] = data['time']
        target_data['interval'] = data['interval']
        target_data['owner_id'] = self._id
        #target_data['motor'] = self.motor

        target = TargetController(self.db, self, data = target_data)
        self.targets.append(target)
        self._update()
        return target


    def get_status(self):
        # Get a list of statuses from the active intervals.
        status_list = []
        for target in self.targets:
            status_list.append(target.get_status())

        return status_list

    def delete(self):
        # Recursively deletes all images associated with the camera,
        # all the data associated with the targets, and finally itself!
        for target in self.targets:
            target.delete()
        # Goodbye!
        self._delete()



# --------------------------------------------------------------------------



class TargetController(ModelController):
    # Handles the individual timelapses, including creation and deletion.
    # A timelapse is a single collection of images from one location.

    def __init__(self, database, camera, data = None, _id = None):
        # Create a model controller object.
        ModelController.__init__(self, 'target', database, data=data, _id=_id)
        self.num_images = 0
        self.queue = Queue(maxsize = 0)
        self.num = 0
        self.camera = camera
        self.interval = Interval(self)
        # self.location = []


    def start(self):
        # Begin capturing data from the microscope.
        int_data = {}
        int_data['time'] = self.model['time']
        int_data['interval'] = self.model['interval']
        int_data['source'] = self.model['source']
        int_data['motor'] = self.model['motor']
        self.interval.begin(int_data)


    def add_image(self, image):
        # Add the image data to this object, and update the database.
        image_data = {}
        image_data['owner_id'] = self._id
        image_data['order'] = self.num
        self.num += 1
        new_image = ImageController(self.db, data = image_data)
        new_image.write_image(image)
        self._update()


    def read(self):
        # Read the current timelapse from the database.
        return self._read


    def get_lapse(self):
        # First, get all of the images stored in the queue.
        while not self.queue.empty():
            self.add_image(self.queue.get())

        # Return a list of all of the encoded images.
        cursor = self.db.image.find({ 'owner_id': self._id })
        images = []

        for img in cursor:
            images.append(pickle.loads(img['image']))

        return images


    def delete(self):
        # First, delete all the images.
        self.db.images.delete_many({ 'owner_id': self._id })

        # Finally, delete myself!
        self._delete()


    def get_status(self):
        # Return the status of the interval
        return [self.interval.status_message, self.interval.is_connected]


    def get_id(self):
        return self._id


# --------------------------------------------------------------------------


class ImageController(ModelController):
    # Handles creating an individual image.

    def __init__(self, database, data = None, _id = None):
        # Initialize an image object.
        # if (_id is None):
        #     data = self.init_new_image(data)

        ModelController.__init__(self, 'image', database, data = data, _id = _id)


    # def init_new_image(self, data):
    #     # Set the new data object to empty.
    #     data['time'] = time.time()
    #     data['image'] = None
    #     data['is_flushed'] = False
    #     data['_id'] = None
    #
    #     return data


    def write_image(self, image):
        # Write an image to the object and push it to the database immediately.
        self.model['image'] = Binary(pickle.dumps(image, protocol = 2))
        self.model['taken_at'] = time.time()
        self.model['is_flushed'] = True
        self._update()


    def read(self):
        # Read the current image from the database.
        self._read()


    @property
    def image(self):
        return self.model['image']


    @property
    def time(self):
        return self.model['time']



# --------------------------------------------------------------------------

if __name__ == '__main__':

    database = connect_to_database()
    session_data = { 'name': 2, 'other': 'stuff', 'number': 1 }

    # Create an arbitrary session.
    session = SessionController(database, data = session_data)

    # Use the first camera connected to the system
    # as a test.  Change index to test other cameras.
    camera_zero = session.add_camera(0)

    # Take five images in five seconds.
    target_data = {
        'x_cord': 0,
        'y_cord': 0,
        'z_cord': 0,
        'time': 5,
        'interval': 1
        }

    target = camera_zero.add_target(target_data)
    statuses = camera_zero.get_status()
    for status in statuses:
        print(status)

    print(target.get_status())

    target.start()

    print(target.get_status())

    print("Running!")

    start = time.time()
    while time.time() < start + 5:
        i = 0

    images = target.get_lapse()

    # Run if you want to see if images are saving correctly,
    # or want to view the images.  They are saved to whatever directory
    # this python file is in.
    # i = 0
    # for img in images:
    #     cv2.imwrite("lapse_img_" + str(i) + ".jpg", img)
    #     i += 1

    # Run if you just need to make sure the interval is working correctly.
    i = 0
    for img in images:
        print("Image " + str(i) + " taken.")
        i += 1


    print("Done! :D")


# --------------------------------------------------------------------------
