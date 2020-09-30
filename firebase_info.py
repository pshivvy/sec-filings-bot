import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('firebase-sdk.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

collection = db.collection('discord-hook-urls')
def get_tickers_by_url(hook_url):
    documents = collection.document(hook_url).get()
    return documents.to_dict()

def set_value(cik, value, hook_url):
    documents = collection.document(hook_url)
    documents.update({
        cik:value
    })

def get_all_data():
    collection = db.collection('discord-hook-urls').stream()
    return list(collection)