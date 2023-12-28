import pymongo
import certifi

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance

    def connect(self, uri):
        if self.client is None:
            try:
                self.client = pymongo.MongoClient(uri,tlsCAFile=certifi.where())
                print("Connected to MongoDB")
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")

    def get_client(self):
        return self.client

    def close(self):
        if self.client is not None:
            self.client.close()
            print("MongoDB connection closed")


def Connect(db_name):
    mongo_conn = MongoDBConnection()
    mongo_conn.connect("mongodb+srv://akhil:akhil@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority")
    client = mongo_conn.get_client()
    if db_name=="users":
        return client.users.users
    if db_name=="clients":
        return client.users.clients
    if db_name=="hotel":
        return client.hotel

if __name__ == "__main__":
    mongo_conn = MongoDBConnection()
    mongo_conn.connect('your_mongodb_uri')
    client = mongo_conn.get_client()
    mongo_conn.close()