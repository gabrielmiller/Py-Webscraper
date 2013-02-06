from datetime import datetime
from settings import *
import database

"""
This module contains functions that would otherwise congest my project
"""

def get_context(input={}):
    """
    Builds the context dictionary for each response.
    """
    context={'year':datetime.today().year}
    if DEBUG == True:
        context['DEBUG']=1
    get_query_string(input.args, context)
    return context

def get_query_string(input=None, context={}):
    """
    Checks the querystring for the parameter "query" and returns its value if
    present. If that parameter is not present it returns null.
    """
    if input:
        context['query'] = input.get('query')
        context['sort'] = input.get('sort')
        context['display'] = input.get('display')
        context['page'] = input.get('page')
        context['results'] = input.get('results')
        return context
    else:
        return None

def build_mongo_query_from_search_terms(input=None, action=None):
    """
    Helper function used to build a mongo query
    """
    input=input.split()
    result = {}
    if action == "select_indices":
        if len(input)<2:
            result['word']=input[0]
            pass
        else:
            result['$or']=[]
            for item in input:
                result['$or'].append({'word':item})
    elif action == "find_indexed_documents":
        pass
    else:
        pass
    return result, action

def query_mongo(query=None, collection=None, action=None, db=None):
    """
    Helper function used to submit a mongo query
    """
    results = None
    if query != None and collection != None and action != None and db != None:
        if action == "select_indices":
            selected_collection = db.dbconnection[collection]
            results = selected_collection.find(query)
        elif action == "select_documents":
            pass
    else:
        pass # You done fucked up son
    return results
