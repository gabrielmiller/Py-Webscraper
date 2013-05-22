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
    context['query'] = input.get('query') if input.get('query') else settings.DEFAULT_QUERY
    context['sort'] = input.get('sort') if input.get('sort') else settings.DEFAULT_SORT
    context['order'] = int(input.get('order')) if input.get('order') else settings.DEFAULT_ORDER
    context['display'] = input.get('display') if input.get('display') else settings.DEFAULT_DISPLAY
    context['page'] = input.get('page') if input.get('page') else settings.DEFAULT_PAGE
    context['results'] = int(input.get('results')) if input.get('results') else settings.DEFAULT_NUMBER_OF_RESULTS
    return context

def get_spider_context(input={}):
    """
    Builds the spider input's context dictionary.
    """
    context={'timestamp':datetime.today()}
    context['url'] = input.get('url') if input.get('url') else None
    context['max_pages'] = input.get('max_pages') if input.get('max_pages') else settings.DEFAULT_MAX_PAGES
    #max frontiers
    #max hops
    #etc.
    return context

def build_queue_input(input={}):
    """
    Constructs the queue input object.
    """
    queue_job = {}
    return queue_job
