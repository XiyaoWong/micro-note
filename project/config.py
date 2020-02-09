import os
import base64


DATABASE = os.path.join(os.path.dirname(__file__), "MicroNote.db")
SECRET_KEY = bytes.decode(base64.b64encode(os.urandom(66)))
DEBUG = True
ENV = 'development'