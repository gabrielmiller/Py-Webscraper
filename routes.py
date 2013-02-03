import os
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from application import *
from database import DatabaseConnection
from functions import *

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
    context = get_context(request)
    return render_template("frontpage.html", context=context)

@app.route("/search")
def search():
    """
    Renders the search results page.
    """
    context = get_context(request)
#    if context.get('query'):
#        search_words = context['query'].split()
#        search_dict = {}
#        if len(search_words)>1:
#            search_dict = {'$or':[]}
#            for item in search_words:
#                search_dict['$or'].append({'word':item})
#        else:
#            search_dict = {'word':search_words[0]}
    dbconnection = DatabaseConnection()
    dbconnection.connect()
    if context.get('query'):
        indices = build_index_dictionary_from_search_terms(context['query'])
        #indices = dbconnection.query_collection(query=context['query'], collection='invertedindex')
        if indices != None:
            pass
        else:
            flash('No results were found', category='text-error')
#    if query_results == None:
#        context['results1'] = None
#    else:
#        context['results1'] = query_results
#        #context['results1']=[]
#        search_dict2={}
#        #for item in query_results:
        #    context['results1'].append(item)
#        
#            if len(item)>1:
#                search_dict2 = {'$or':[]}
#                for object in item:
#                     search_dict2['$or'].append({'url':object['url']})
#            else:
#                for object in item:
#                    search_dict2['url']=object['url']
#        
    return render_template("search.html", context=context)

@app.route("/spider")
def spider():
    """
    Renders the spider dashboard page.
    """
    context = get_context(request)
    return render_template("spider.html", context=context)

@app.route("/addspider", methods=["GET","POST"])
def addspider():
    """
    Post requests to this url will add a spider.
    """
    if request.method == 'POST':
        flash('Error: Adding spiders is not yet implemented. Try again later!', category='text-error')
    return redirect(url_for('frontpage'))
