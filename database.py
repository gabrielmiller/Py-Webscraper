from pymongo import Connection
from pymongo.errors import ConnectionFailure
import settings
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
            connection = Connection(host=settings.DATABASE_HOST, port=settings.DATABASE_PORT)
        except ConnectionFailure, error:
            return "Could not connect to database: %s" % error
            print "Could not connect to database: %s \n" % error
            if __name__ == "spider":
                sys.exit(1)
        self.dbconnection = connection[settings.DATABASE_NAME]

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

def query_mongo(query=None, collection=None, db=None, sort=settings.DEFAULT_SORT, number_of_results=settings.DEFAULT_NUMBER_OF_RESULTS, order=settings.DEFAULT_ORDER):
    """
    Submits a select query to mongodb.
    """
    if sort == 'rel':
        sort = 'pagerank'
    elif sort == 'dat':
        sort = 'date'
    elif sort == 'len':
        pass
    elif sort == 'cha':
        pass
    else:
        sort = None
    if query != None and collection != None and db != None:
        selected_collection = db.dbconnection[collection]
        cursor = selected_collection.find(query).sort(sort, order).limit(number_of_results)
        results_count = cursor.count()
        if collection == settings.COLLECTION_INDEX:
            results = {}
            for item in cursor:
                results[item['word']] = item['index']
        elif collection == settings.COLLECTION_DOCUMENTS:
            results = []
            for item in cursor:
                results.append(item)
        return results, results_count
    else:
        return [], 0
