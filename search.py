import os
from flask import render_template, redirect, url_for, request, flash
from application import *

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'assets'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
    def frontpage():
        return render_template("frontpage.html", context=context)

@app.route("/search")
    def search():
        return render_template("search.html", context=context)

@app.route("/spider")
    def spider():
        return render_template("spider.html", context=context)
