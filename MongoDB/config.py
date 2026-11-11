import os
import sys
from typing import Tuple

try:
    from pymongo import MongoClient
    from pymongo.database import Database
except ImportError:
    print(
        "[ERROR] PyMongo is not installed. Run: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

DEFAULT_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "urban_waste_db"

COLLECTION_INCIDENTS = "hazardousIncidents"
COLLECTION_INSPECTIONS = "patrolInspections"

VALID_INCIDENT_STATUSES = [
    "Open",
    "Under Inspection",
    "Remediated",
    "Closed",
]

def get_database(uri: str = DEFAULT_URI) -> Tuple[MongoClient, Database]:
    client: MongoClient = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db: Database = client[DB_NAME]
    return client, db