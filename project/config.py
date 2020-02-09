import os
import base64



DATABASE = 'MicroNote.db'
SECRET_KEY = str.encode(base64.b64encode(os.urandom(66)))
DEBUG = True
ENV = 'development'