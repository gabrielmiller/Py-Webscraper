from datetime import datetime
import settings
import database

"""
This module contains helper functions.
"""

def remove_duplicate_dictionaries(input):
    """
    Removes duplicate dictionarise from a list of dictionaries.
    """
    if type(input) != list:
        raise("remove_duplicate_dictionaries requires a list input.")
    return [dict(a_tuple) for a_tuple in set(tuple(item.items()) for item in input)]

def remove_duplicate_numbers(input):
    """
    Removes duplicate numbers from a list of numbers.
    """
    if type(input) != list:
        raise("remove_duplicate_numbers requires a list input.")
    return list(set(input))

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
