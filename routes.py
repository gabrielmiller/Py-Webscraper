import os
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from application import *
import database
import functions

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
    context = functions.get_context(request)
    return render_template("frontpage.html", context=context)

@app.route("/search")
def search():
    """
    Renders the search results page.
    """
    context = functions.get_context(request)
    dbconnection = database.DatabaseConnection()
    dbconnection.connect()
    if context.get('query'):
        mongo_query, action = functions.build_mongo_query_from_search_terms(input=context['query'], action="select_indices")
        #flash('query: '+str(mongo_query), category='text-info')
        if mongo_query != None:
            cursor = functions.query_mongo(query=mongo_query, collection="indicies", action=action, db=dbconnection)
            results = ""
            for item in cursor:
                results += str(item['index'])
            if results:
                flash('Results were found: '+results, category='text-info')
            #iterate through results
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
    context = functions.get_context(request)
    return render_template("spider.html", context=context)

@app.route("/addspider", methods=["GET","POST"])
def addspider():
    """
    Post requests to this url will add a spider.
    """
    if request.method == 'POST':
        flash('Error: Adding spiders is not yet implemented. Try again later!', category='text-error')
    return redirect(url_for('frontpage'))
