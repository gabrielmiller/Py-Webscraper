import os
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from application import *
"""
This module contains the routing and logic for the search front-end side of
this website
"""

def get_query_string():
    """
    This function checks the querystring for the parameter "query" and returns its
    value if present. If that parameter is not present it returns null.
    """
    if request.args.get('query'):
        context = dict()
        context['query'] = request.args.get('query')
        context['sort'] = request.args.get('sort')
        context['display'] = request.args.get('display')
        context['page'] = request.args.get('page')
        context['results'] = request.args.get('results')
        return context
    else:
        return None

@app.route("/favicon.ico")
def favicon():
    """
    Returns the URL for the favicon dynamically.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def frontpage():
    """
    Renders the search splash page.
    """
    context = get_query_string()
    return render_template("frontpage.html", context=context)

@app.route("/search")
def search():
    """
    Renders the search results page.
    """
    context = get_query_string()
    return render_template("search.html", context=context)

@app.route("/spider")
def spider():
    """
    Renders the spider dashboard page.
    """
    context = get_query_string()
    return render_template("spider.html", context=context)
