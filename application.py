from flask import Flask

"""
This module contains the application boilerplate for the website front-end
of this web application.
"""

app = Flask("Toastie")

from routes import *

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
