#-------------------------------------------------------------------------
# AUTHOR: Wesley Dam
# FILENAME: db_connection_mongo.py
# SPECIFICATION: This script connects to a MongoDB database and provides functions
#                to create, delete, update, and retrieve documents with text analysis.
# FOR: CS 4250- Assignment #2
# TIME SPENT: 5 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
from pymongo import MongoClient
import string

def connectDataBase():
    # Create a database connection object using pymongo
    DB_NAME = "cs4250"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db
    
    except:
        print("Could not connect to MongoDB")

def createDocument(col, docId, docText, docTitle, docDate, docCat):
    # remove punctuation from the text
    docText = docText.translate(str.maketrans('', '', string.punctuation))

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    term_count = {}
    terms = docText.lower().split(" ")
    for term in terms:
        if term in term_count:
            term_count[term] += 1
        else:
            term_count[term] = 1

    # create a list of dictionaries to include term objects. [{"term", count, num_char}]
    term_objects = [
        {
            "term": term,
            "count": term_count[term],
            "num_chars": len(term)
        }
        for term in term_count
    ]

    #Producing a final document as a dictionary including all the required document fields
    document = {
        "doc": docId,
        "text": docText,
        "title": docTitle,
        "num_chars": sum([len(term) for term in term_count]),
        "date": docDate,
        "category": docCat,
        "terms": term_objects
    }

    # Insert the document
    col.insert_one(document)

def deleteDocument(col, docId):
    # Delete the document from the database
    col.delete_one({"doc": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Delete the document
    deleteDocument(col, docId)
    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    index = {}

    for doc in col.find():
        for term_object in doc["terms"]:
            term = term_object["term"]
            count = term_object["count"]

            if term in index:
                index[term] += f",{doc['title']}:{count}"
            else:
                index[term] = f"{doc['title']}:{count}"

    return dict(sorted(index.items()))