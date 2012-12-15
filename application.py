from flask import Flask

"""
This module contains the application boilerplate for the website front-end
of this web application.
"""

app = Flask("Toastie")

app.secret_key = '143d35gBxl3[f50%4qWWr431pomRL;1qdc-dffdCX123554hgH&KnL44b0,23'

from routes import *

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
