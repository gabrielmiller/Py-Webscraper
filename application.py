from flask import Flask

app = Flask("Toastie")

app.secret_key = '143d35gBxl3[f50%4qWWr431pomRL;1qdc-dffdCX123554hgH&KnL44b0,23'

from search import *

if __name__ == "__main__"
    app.debug = True
    app.run(host='0.0.0.0')
