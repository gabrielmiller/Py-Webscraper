from datetime import datetime
import settings
import database

"""
This module contains helper functions.
"""

def get_context(input={}):
    """
    Builds the page context dictionary for each response.
    """
    context={'year':datetime.today().year}
    if settings.DEBUG == True:
        context['DEBUG']=1
    get_query_string(input.args, context)
    return context

def get_query_string(input=None, context={}):
    """
    Checks the query string for the parameter "query" and returns its value if
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

def build_mongo_index_query(input=None):
    """
    Builds a mongo query to look up indices from the given cursor.
    """
    result = {}
    input=input.split()
    if len(input)<2:
        result['word']=input[0]
    else:
        result['$or']=[]
        for item in input:
            result['$or'].append({'word':item})
    return result

def build_mongo_pages_query(input=None):
    """
    Builds a mongo query to look up documents from the given cursor.
    """
    result = {}
    #input=input.split()
    #for word in input:
    #    for index in word:
    #        pass
    #        # Concatenate words and indices to build a query
    return result

def query_mongo_index(query=None, collection=None, db=None):
    """
    Submits a query regarding indices to mongodb.
    """
    results = None
    if query != None and collection != None and db != None:
        selected_collection = db.dbconnection[collection]
        cursor = selected_collection.find(query)
        results = {}
        results_count = cursor.count()
        for item in cursor:
            results[item['word']] = item['index']
        return results, results_count
    else:
        pass # You done fucked up son

def query_mongo_pages(query=None, collection=None, db=None):
    """
    Submits a query regarding pages to mongodb.
    """
    pass

def combine_cursors(input=None):
    """
    Combines mongo query cursor dictionaries.
    """
    output = {}
    if type(input)==dict:
        for subdictionary_key in input:
            for item_key in input[subdictionary_key]:
                if output.get(item_key):
                    output[item_key] = output[item_key] + input[subdictionary_key][item_key]
                else:
                    output[item_key] = input[subdictionary_key][item_key]
        return output
    else:
        return "Error: You didn't feed me a dictionary"
