import sys
from typing import Optional
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError
from MongoDB.config import (
    COLLECTION_INCIDENTS,
    COLLECTION_INSPECTIONS,
    DB_NAME,
    DEFAULT_URI,
    get_database,
)
from MongoDB.crud import (
    add_new_document,
    delete_existing_document,
    display_all_documents,
    search_documents,
    update_existing_document,
)

def select_collection(db: Database) -> Optional[Collection]:
    while True:
        print("\n" + "=" * 68)
        print(" DUBLIN CITY COUNCIL - HAZARDOUS WASTE MANAGEMENT SYSTEM (MongoDB)")
        print("=" * 68)
        print("Select a collection to work with:")
        print(f"  1. {COLLECTION_INCIDENTS} (Citizen & Sensor Hazardous Waste Reports)")
        print(f"  2. {COLLECTION_INSPECTIONS} (Enforcement Patrols, Fines & Cleanups)")
        print("  6. Exit System")
        choice = input("\nEnter choice (1, 2, or 6 to Exit): ").strip()

        if choice == "1":
            return db[COLLECTION_INCIDENTS]
        if choice == "2":
            return db[COLLECTION_INSPECTIONS]
        if choice in ("6", "q", "exit"):
            return None
        print("[!] Invalid choice. Please enter 1, 2, or 6.")

def collection_menu(db: Database) -> None:
    while True:
        collection = select_collection(db)
        if collection is None:
            print("\nExiting Hazardous Waste Management System. Goodbye!")
            return

        while True:
            print("\n" + "-" * 68)
            print(f" Active Collection: {collection.name} (Database: {DB_NAME})")
            print("-" * 68)
            print("  1. Display all the documents in the chosen collection (Read / Find)")
            print("  2. Add a new document to the chosen collection (Create)")
            print("  3. Update an existing document in that collection (Update)")
            print("  4. Delete an existing document in that collection (Delete)")
            print("  5. Search for documents using a text input / keyword filter (Search)")
            print("  0. Switch collection")
            print("  6. Exit System")

            action = input("\nSelect an option (1-6, or 0 to switch collection): ").strip()

            if action == "1":
                display_all_documents(collection)
            elif action == "2":
                add_new_document(collection)
            elif action == "3":
                update_existing_document(collection)
            elif action == "4":
                delete_existing_document(collection)
            elif action == "5":
                search_documents(collection)
            elif action == "0":
                break
            elif action in ("6", "q", "exit"):
                print("\nExiting Hazardous Waste Management System. Goodbye!")
                return
            else:
                print(
                    "[!] Invalid option. Please enter a number from 1 to 6 "
                    "(or 0 to switch collection)."
                )

def run_app() -> None:
    print(f"Connecting to MongoDB at {DEFAULT_URI} (Database: {DB_NAME})...")
    client = None
    try:
        client, db = get_database(DEFAULT_URI)
        collection_menu(db)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting system.")
    except PyMongoError as exc:
        print(f"\n[ERROR] Database connection error: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        if client is not None:
            client.close()