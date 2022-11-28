from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app,  default_mediatype='application/xml')

from src import routes
