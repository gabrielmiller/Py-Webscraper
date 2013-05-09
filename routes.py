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
    Returns the URL for the favicon dynamically.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def frontpage():
    """
    Renders the search splash page.
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
        mongo_query, action = helpers.build_mongo_query(input=context['query'], action="select_indices")
        #flash('query: '+str(mongo_query), category='text-info')
        if mongo_query != None:
            cursor, cursor_count = helpers.query_mongo(query=mongo_query, collection=settings.COLLECTION_INDEX, action=action, db=dbconnection)
            context['cursor'] = cursor
            context['cursor_count'] = cursor_count
            if cursor_count > 1:
                cursor = helpers.combine_cursors(cursor)
            context['combined_cursor'] = cursor
            #documents = helpers.query_mongo(query=cursor, collection=settings.COLLECTION_DOCUMENTS, action="select_documents")
            #results = ""
            #for item in cursor:
            #    results += str(item)
            #if results:
            flash('Results: '+str(cursor), category='text-info')
            #iterate through results
        else:
            flash('No results were found', category='text-error')
#        
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
