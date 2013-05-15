from pymongo import Connection
from pymongo.errors import ConnectionFailure
from settings import *
import helpers

class DatabaseConnection():
    """
    Initiates a database connection and sets up data insertion/querying
    """

    def connect(self):
        """
        Establishes a database connection
        """
        try:
            connection = Connection(host=DATABASE_HOST, port=DATABASE_PORT)
        except ConnectionFailure, error:
            return "Could not connect to database: %s" % error
            print "Could not connect to database: %s \n" % error
            if __name__ == "spider":
                sys.exit(1)
        self.dbconnection = connection[DATABASE_NAME]

def build_mongo_index_query(input=None):
    """
    Builds a mongo query to look up indices from the given cursor.
    """
    result = {}
    input=input.split()
    if len(input) < 2:
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
    result, hits = {}, {}
    result['$or'] = []
    if len(input) > 1:
        for word in input:
            for url in input[word]:
                result['$or'].append({'url':url})
                for word_number in input[word][url]:
                    #print word, url, word_number, input[word][url], input[word][url][word_number]
                    #print word, url, word_number, input[word][url] #, input[word][url][word_number]
                    if hits.get(url):
                        hits[url].append(word_number)
                    else:
                        hits[url] = [word_number]
        for key in hits:
            hits[key] = helpers.remove_duplicate_numbers(hits[key])
        result['$or'] = helpers.remove_duplicate_dictionaries(result['$or'])
    else:
        for search_word in input:
            for url in input[search_word]:
                hits[url] = input[search_word][url]
                result['$or'].append({'url':url})
    return result, hits

def query_mongo(query=None, collection=None, db=None):
    """
    Submits a select query to mongodb.
    """
    results = None
    if query != None and collection != None and db != None:
        selected_collection = db.dbconnection[collection]
        cursor = selected_collection.find(query)
        results = {}
        results_count = cursor.count()
        if collection = COLLECTION_INDEX:
            for item in cursor:
                results[item['word']] = item['index']
        else if collection = COLLECTION_DOCUMENTS:
            for item in cursor:
                results[item['pages']] = item['index']
        return results, results_count
    else:
        return None, None
