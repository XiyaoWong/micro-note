import os
import base64


DATABASE = os.path.join(os.path.dirname(__file__), "MicroNote.db")
SECRET_KEY = "your secret key"
DEBUG = False
ENV = 'production'