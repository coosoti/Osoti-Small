""" Configurations
"""

import os
from dotenv import load_dotenv

load_dotenv() 


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

JSON_SORT_KEYS = False


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')	