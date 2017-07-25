import numpy as np
import time
from pymongo import MongoClient
from bson import ObjectId

# Interface for dealing with a Mongo database.

def connect_to_database(database_name = 'mvs_dev'):
    # Establish a connection to the database.
    client = MongoClient()
    database = client[database_name]
    return database


def created_at():
    # Return a date/time string.
    return time.strftime('%Y-%m-%d@%H:%M:%S', time.localtime())


def unix_time_in_microseconds():
    # Return current POSIX epoch in microseconds, as a 64-bit integer
    return np.int64(time.time() * 1e6)


def q(record):
    return record['_id']


def qry(record):
    # Return a query object for the specified record.
    return { '_id': q(record) }


def qwrap(_id):
    # Wrap an _id object in a query dict.
    return { '_id': _id }


def get_latest(record, collection):
    # Get the latest version of the record.
    return collection.find_one(qry(record))


def find_unique_resource(collection):
    return collection.find_one()


def update_document(document, collection):
    # Update the given document in the collection.
    query = { '_id': document['_id'] }
    collection.update_one(query, { '$set': document }, upsert = False)


def find_document(document_id, collection):
    # Find a document in a collection with a given id.
    query = { '_id': string_to_obj(document_id) }
    return collection.find_one(query)


def find_inserted_document(insertion_response, collection):
    # Get the most recently inserted document.
    if (insertion_response) and (insertion_response.acknowledged):
        doc = collection.find_one({ '_id': insertion_response.inserted_id })
    else:
        doc = None
    return doc


def string_to_obj(string):
    return ObjectId(string)



def goodify(obj):
    # Loop through a mongo object and convert '_id' field to a string.
    if '_id' in obj:
        obj['_id'] = str(obj['_id'])
    return obj


def serialize_mongo(result):
    # If it is a list, iterate over it.
    if type(result) == list:
        out = []
        for obj in result:
            out.append(goodify(obj))
        return out
    else:
        out = goodify(result)
    return out
