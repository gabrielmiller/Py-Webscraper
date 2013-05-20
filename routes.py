import os
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from application import *
import database
import helpers
import settings

"""
This module contains the routing for the search front-end of the website.
"""

@app.route("/favicon.ico")
def favicon():
    """
    Serves the favicon through the app.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def frontpage():
    """
    Renders the front page.
    """
    context = helpers.get_context(request)
    return render_template("frontpage.html", context=context)

@app.route("/search")
def search():
    """
    Renders the search results page.
    """
    context = helpers.get_context(request)
    dbconnection = database.DatabaseConnection()
    dbconnection.connect()
    if context.get('query'):
        query_index = database.build_mongo_index_query(input=context['query'])
        #flash('query: '+str(mongo_query), category='text-info')
        context['query_index'] = query_index
        if query_index != None:
            cursor, cursor_count = database.query_mongo(query=query_index, collection=settings.COLLECTION_INDEX, db=dbconnection)
            context['cursor'] = cursor
            context['cursor_count'] = cursor_count
            query_pages, query_pages_hits = database.build_mongo_pages_query(input=cursor)
            context['query_pages'] = query_pages
            context['query_pages_hits'] = query_pages_hits
            documents, documents_count = database.query_mongo(query=query_pages, collection=settings.COLLECTION_DOCUMENTS, db=dbconnection, sort=context['sort'], number_of_results=context['results'], order=context['order'])
            context['documents'] = documents
            context['documents_count'] = documents_count
            if(context['documents_count'] == 0):
                flash('No results were found.', category='text-error')
        else:
            flash('No results were found.', category='text-error')
    return render_template("search.html", context=context)

@app.route("/spider")
def spider():
    """
    Renders the spider dashboard page.
    """
    context = helpers.get_context(request)
    return render_template("spider.html", context=context)

@app.route("/addspider", methods=["GET","POST"])
def addspider():
    """
    Post requests to this url will add a spider.
    """
    if request.method == 'POST':
        flash('Error: Adding spiders is not yet implemented. Try again later!', category='text-error')
    return redirect(url_for('frontpage'))
