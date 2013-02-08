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
        self.dbconnection = connection["ex14"]
