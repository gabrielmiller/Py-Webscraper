"""
This module contains site settings.
"""

# Print query variables to the page
DEBUG = True
COLLECTION_INDEX = 'index'
COLLECTION_DOCUMENTS = 'pages'

#Database Settings
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 27017
DATABASE_NAME = "toastie"

#Default Search Settings
DEFAULT_SORT = "rel"
DEFAULT_ORDER = -1
DEFAULT_NUMBER_OF_RESULTS = 10
DEFAULT_PAGE = 1
DEFAULT_DISPLAY = None
DEFAULT_QUERY = ""
