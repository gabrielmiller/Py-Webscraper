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

    def query(self, collection='junkdata', context=None):
        """
        Query data out of the collection
        """
        if self.dbd:
            self.dbc = self.dbd[collection]
            self.results = self.dbc.find(context)
            self.returnlist = []
            for items in self.results:
                self.returnlist.append(items)
            return self.returnlist
        else:
            return None

