from datetime import datetime
from settings import *

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

def build_index_dictionary_from_search_terms(input=None):
    """
    Looks up the search terms in the index and returns a dictionary of the
    locations of the word(s)
    """
    input=input.split()
    return build_mongo_query(input=input, action="select_indices")

def build_mongo_query(input=None, action=None):
    """
    Helper function used to build a mongo query
    """
    result = {}
    if action == "select_indices":
        if len(input)<2:
            result['word']=item
            pass
        else:
            result['$or']=[]
            for item in input:
                result['$or'].append({'word':item})
    elif action == "find_indexed_documents":
        pass
    else:
        pass
    return result
