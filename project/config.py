import os
import base64


DATABASE = os.path.join(os.path.dirname(__file__), "MicroNote.db")
SECRET_KEY = base64.b64encode(os.urandom(66)).decode('utf-8')
DEBUG = False
ENV = 'production'
