from pymongo import Connection
from pymongo.errors import ConnectionFailure

class DatabaseConnection():
    """
    Initiates a database connection and sets up data insertion/querying
    """

    def connect(self):
        """
        Establishes a database connection
        """
        try:
            connection = Connection(host="localhost", port=27017)
        except ConnectionFailure, error:
            return "Could not connect to database: %s" % error
            print "Could not connect to database: %s \n" % error
            if __name__ == "spider":
                sys.exit(1)
        self.dbd = connection["ex14"]

    def load_document(self, document):
        """
        Record the document to that was passed in as a dictionary
        """
        self.document = document

    def insert_document(self, collection='junkdata'):
        """
        Insert the document into the database, into the provided collection
        """
        if self.document and self.dbd:
            self.dbc = self.dbd[collection]
            self.dbc.insert(self.document, safe=True)

    def query_index(self, context=None):
        """
        Query data out of the collection
        """
        if self.dbd:
            self.dbc = self.dbd['invertedindex']
            self.results = self.dbc.find(context)
            self.returndict = {}
            self.numitems = 0
            for items in self.results:
                if self.numitems == 1:
                    if not self.returndict.get('$or'):
                        self.returndict['$or'] = []
                    try:
                        self.returndict.pop(['url'])
                    except:
                        self.returndict['$or'].append({'url':items['hits']['url']})
                if self.numitems == 0:
                    self.returndict['url'] = items['hits']['url']
                self.numitems += 1

            return self.returndict
        else:
            return None

    def query_webpages(self, context=None):
        """
        Query data out of the collection
        """
        if self.dbd:
            self.dbc = self.dbd['scrapedata']
            self.results = self.dbc.find(context)
            self.returnlist = []
            for items in self.results:
                self.returnlist.append(items)
            return self.returnlist
        else:
            return None


