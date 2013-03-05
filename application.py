from flask import Flask
"""
This module contains the application boilerplate for the website front-end
of this web application.
"""

app = Flask("Toastie")
app.secret_key = '11jTNgf;d34%44j)294dnQ0dfg$443fjjdPq4RT332'

from routes import *

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
