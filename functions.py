"""
This module would contain functions that would otherwise congest my project
"""

def get_query_string(input=None):
    """
    This function checks the querystring for the parameter "query" and returns its
    value if present. If that parameter is not present it returns null.
    """
    if input:
        context = dict()
        context['query'] = input.get('query')
        context['sort'] = input.get('sort')
        context['display'] = input.get('display')
        context['page'] = input.get('page')
        context['results'] = input.get('results')
        return context
    else:
        return None

