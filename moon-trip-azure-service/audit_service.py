import datetime
import logging
import os
import uuid

from azure.cosmos import CosmosClient, PartitionKey
import firebase_admin
from firebase_admin import credentials, firestore

# --- Setup logging ---
logging.basicConfig(level=logging.INFO)

# --- Firebase Setup ---
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate('../moon-trip-google-service/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)

def fetch_data_from_firebase():
    init_firebase()
    db = firestore.client()
    docs = db.collection('your_collection').stream()

    values = []
    for doc in docs:
        d = doc.to_dict()
        if 'value' in d:
            values.append(d['value'])
    return values

# --- Data Analysis ---
def summarize_data(data):
    if not data:
        return {}

    return {
        "count": len(data),
        "total": sum(data),
        "average": sum(data) / len(data),
        "max": max(data),
        "min": min(data)
    }

# --- Cosmos DB Setup ---
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DB = "cosmo-db134"
COSMOS_CONTAINER = "WeeklySummary"

def write_to_cosmos(summary_data):
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.create_database_if_not_exists(id=COSMOS_DB)
    container = db.create_container_if_not_exists(
        id=COSMOS_CONTAINER,
        partition_key=PartitionKey(path="/partitionKey"),
        offer_throughput=400
    )

    item = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "summary": summary_data,
        "partitionKey": "weekly"
    }

    container.upsert_item(item)
    return item["id"]

# --- Main Execution ---
def main():
    logging.info("Starting weekly audit job...")

    try:
        data = fetch_data_from_firebase()
        summary = summarize_data(data)
        doc_id = write_to_cosmos(summary)
        logging.info(f"Audit summary written to Cosmos DB with ID: {doc_id}")
    except Exception as e:
        logging.error("Error during audit job: %s", str(e))

if __name__ == "__main__":
    main()
