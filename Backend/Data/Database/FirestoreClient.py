import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional
import os

class FirestoreClient:
    """Singleton class to manage Firestore database connection"""
    _instance: Optional['FirestoreClient'] = None
    _db: Optional[firestore.Client] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._db:
            # Initialize Firebase Admin SDK if not already initialized
            if not firebase_admin._apps:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                cred_path = os.path.join(current_dir, 'serviceAccountKey.json')
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            self._db = firestore.client()
    
    @property
    def db(self) -> firestore.Client:
        """Get the Firestore client instance"""
        return self._db
    
    def get_collection(self, collection_name: str) -> firestore.CollectionReference:
        """Get a reference to a Firestore collection"""
        return self._db.collection(collection_name)
    
    def get_document(self, collection_name: str, document_id: str) -> firestore.DocumentReference:
        """Get a reference to a Firestore document"""
        return self._db.collection(collection_name).document(document_id) 