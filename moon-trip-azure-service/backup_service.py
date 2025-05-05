from azure.storage.blob import BlobServiceClient
from firebase_admin import credentials, firestore
import firebase_admin
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Blob Storage configuration
#get connection string from env
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# Initialize Firebase
cred = credentials.Certificate('moon-trip-google-service\serviceAccountKey.json') 
firebase_admin.initialize_app(cred)
db = firestore.client()

def initialize_azure_storage():
    """Initialize Azure Blob Storage client and create container if it doesn't exist."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # Create container if it doesn't exist
        if not container_client.exists():
            container_client.create_container()
            
        return container_client
    except Exception as e:
        print(f"Error initializing Azure Storage: {str(e)}")
        raise

def backup_collection(collection_name):
    """Backup a Firestore collection to a JSON file."""
    try:
        # Get all documents from the collection
        collection_ref = db.collection(collection_name)
        documents = collection_ref.stream()
        
        # Convert documents to dictionary
        data = []
        for doc in documents:
            doc_dict = doc.to_dict()
            doc_dict['id'] = doc.id
            data.append(doc_dict)
            
        return data
    except Exception as e:
        print(f"Error backing up collection {collection_name}: {str(e)}")
        raise

def upload_to_blob_storage(container_client, data, collection_name):
    """Upload JSON data to Azure Blob Storage."""
    try:
        # Create timestamp for the backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"{collection_name}_{timestamp}.json"
        
        # Convert data to JSON string
        json_data = json.dumps(data, default=str)
        
        # Upload to blob storage
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json_data, overwrite=True)
        
        print(f"Successfully uploaded backup for {collection_name} to {blob_name}")
        return blob_name
    except Exception as e:
        print(f"Error uploading to blob storage: {str(e)}")
        raise

def create_backup():
    """Create a complete backup of all Firestore collections."""
    try:
        # Initialize Azure Storage
        container_client = initialize_azure_storage()
        
        # Collections to backup
        collections = ['users', 'tasks']
        
        backup_results = {}
        for collection in collections:
            # Backup collection
            data = backup_collection(collection)
            
            # Upload to blob storage
            blob_name = upload_to_blob_storage(container_client, data, collection)
            backup_results[collection] = blob_name
            
        return backup_results
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        results = create_backup()
        print("Backup completed successfully!")
        print("Backup files:", results)
    except Exception as e:
        print(f"Backup failed: {str(e)}") 