import sys
import numpy as np
from flask import Flask, request, abort
from time import time, sleep
from flask_restful import abort, Api, Resource, reqparse
from flask_cors import *
from gevent.wsgi import WSGIServer



# Create a RESTFUL web server
app = Flask(__name__)
api = Api(app)
valid_headers = ['Content-Type', 'Access-Control-Allow-Origin', '*']
cors = CORS(app, allow_headers=valid_headers)

client = MongoClient()
