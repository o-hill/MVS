from pymongo import MongoClient
from database import *
import logging as log
from bson import ObjectId
import time
import cv2
from intervals import Interval


# --------------------------------------------------------------------------


class ModelController(object):
    # Base class for dealing with models and saving to databases.


    def __init__(self, model_name, database, data = None, _id = None):
        # Connect to a database.  Load or create the model.
        self.db = database
        self.model_name = model_name
        self.collection = self.db[model_name]

        # Logging?
        log.basicConfig(level = verbose)
        self.log = log.getLogger(__name__)

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
            self.log.info('> Attempting to create a new model in {:s}'.\
                format(self.model_name))

            try:
                insertion = self.collection.insert_one(data)
            except:
                self.log.exception('> Critical error in creating {:s}.'.\
                    format(self.model_name))

            self.log.info('> Created a new model in {:s}'.format(self.model_name))
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
        self.log.info(' > Updating current model in {:s}'.format(self.\
                model_name))
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
        lapses = []


    def read(self):
        # Read a specific session from the database.
        self._read()
        if self.model:
            self.load_series()
            self.load_annotations()


    def load_annotations(self):
        # Load all annotations.
        query = {}
        query['owner_id'] = self._id
        self.annotations = list(self.db.annotations.find(query))
        self.model['annotations'] = self.annotations

    #
    # def delete(self): # NOT SURE ABOUT THIS YET.
    #     # Delete the current session and all associated time series.
    #     # First find all the time series I own, and delete those.
    #     cursor = self.db.time_series.find({ 'owner_id': self._id })
    #     for ts in cursor


# --------------------------------------------------------------------------



class CameraController(ModelController):
    # Deals with an individual camera in the system.

    def __init__(self, database, data = None, _id = None):
        # Initialize as a camera object.
        ModelController.__init__(self, 'camera', database, data=data, _id=_id)
        # A source number must be specified.
        self.source = data['source']
        # Blank list of targets belonging to the camera.
        targets = []

    def read(self):
        # Read the current camera from the database.
        self._read()


    def add_target(self, data):
        # Required data points:
        #   x_cord, y_cord, z_cord for positioning camera
        #   Total amount of time to take images for.
        #   Interval time.
        target_data = {}
        target_data['x_cord'] = data['x_cord']
        target_data['y_cord'] = data['y_cord']
        target_data['z_cord'] = data['z_cord']
        target_data['source'] = self.source
        target_data['time'] = data['time']
        target_data['interval'] = data['interval']
        target_data['owner_id'] = self._id

        target = TargetController(database, data = target_data)
        self.targets.append(target._id)
        self._update()


    def delete(self):
        # Recursively deletes all images associated with the camera,
        # all the data associated with the targets, and finally itself!
        for target in targets:
            target.delete()
        # Goodbye!
        self._delete()


# --------------------------------------------------------------------------



class TargetController(ModelController):
    # Handles the individual timelapses, including creation and deletion.
    # A timelapse is a single collection of images from one location.

    def __init__(self, database, data = None, _id = None):
        # Create a model controller object.
        ModelController.__init__(self, database, data=data, _id=_id)
        self.num_images = 0
        # self.location = []


    def start(self):
        # Begin capturing data from the microscope.
        interval = Interval(self)
        interval.begin(data['time'], data['interval'], data['source'])


    def add_image(self, image):
        # Add the image data to this object, and update the database.
        image_data = {}
        image_data['owner_id'] = self._id
        new_image = ImageController(self.db, data = image_data)
        new_image.write_image(image)
        self._update()


    def read(self):
        # Read the current timelapse from the database.
        return self._read


    def get_lapse(self):
        # Return a list of the encoded images.
        cursor = self.db.images.find({ 'owner_id': self._id })
        images = []

        for img in cursor:
            images.append(img['image'])

        return images


    def delete(self):
        # First, delete all the images.
        self.db.images.delete_many({ 'owner_id': self._id })

        # Finally, delete myself!
        self._delete()


    def get_id(self):
        return self._id


# --------------------------------------------------------------------------


class ImageController(ModelController):
    # Handles creating an individual image.

    def __init__(self, database, data = None, _id = None):
        # Initialize an image object.
        if (_id is None):
            data = self.init_new_image(data)

        ModelController(self, 'images', database, data, _id)


    def init_new_image(self, data):
        # Set the new data object to empty.
        data['time'] = time.time()
        data['image'] = None
        data['is_flushed'] = False
        data['_id'] = None

        return data


    def write_image(self, image):
        # Write an image to the object and push it to the database immediately.
        data['image'] = image
        data['taken_at'] = time.time()
        data['is_flushed'] = True
        self._update()


    def read(self):
        # Read the current image from the database.
        self._read()


    @property
    def image(self):
        return data['image']

    @property
    def time(self):
        return data['time']



# --------------------------------------------------------------------------
