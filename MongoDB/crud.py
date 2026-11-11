import re
from typing import Any, Dict
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from MongoDB.config import COLLECTION_INCIDENTS
from MongoDB.models import build_new_incident_doc, build_new_inspection_doc
from MongoDB.utils import (
    build_identifier_filter,
    pretty_print_doc,
    prompt_bool,
    prompt_float,
    prompt_str,
)

def display_all_documents(collection: Collection) -> None:
    print(f"\n=== [1] DISPLAY ALL DOCUMENTS IN '{collection.name}' ===")
    try:
        docs = list(collection.find())
        if not docs:
            print(f"No documents found in '{collection.name}'.")
            return
        for idx, doc in enumerate(docs, start=1):
            pretty_print_doc(doc, idx)
        print(f"\nTotal documents in '{collection.name}': {len(docs)}")
    except PyMongoError as exc:
        print(f"[ERROR] Failed to read documents: {exc}")

def add_new_document(collection: Collection) -> None:
    print(f"\n=== [2] ADD NEW DOCUMENT TO '{collection.name}' ===")
    try:
        if collection.name == COLLECTION_INCIDENTS:
            new_doc = build_new_incident_doc()
        else:
            new_doc = build_new_inspection_doc()

        result = collection.insert_one(new_doc)
        print(
            f"\n[SUCCESS] Document inserted into '{collection.name}' "
            f"with _id: {result.inserted_id}"
        )
        pretty_print_doc(new_doc)
    except PyMongoError as exc:
        print(f"[ERROR] Failed to insert document: {exc}")

def update_existing_document(collection: Collection) -> None:
    print(f"\n=== [3] UPDATE EXISTING DOCUMENT IN '{collection.name}' ===")
    key_label = (
        "incident_id (e.g. INC-2026-001)"
        if collection.name == COLLECTION_INCIDENTS
        else "inspection_id (e.g. INS-2026-8801)"
    )
    identifier = prompt_str(f"Enter {key_label} or _id to update")
    query_filter = build_identifier_filter(collection.name, identifier)

    try:
        existing = collection.find_one(query_filter)
        if not existing:
            print(f"[!] No document found matching '{identifier}'.")
            return

        print("\nCurrent Document:")
        pretty_print_doc(existing)

        update_fields: Dict[str, Any] = {}
        if collection.name == COLLECTION_INCIDENTS:
            print(
                "\nSelect field to update in 'hazardousIncidents':\n"
                "  1. status (Open / Under Inspection / Remediated / Closed)\n"
                "  2. is_contained (Boolean)\n"
                "  3. hazard_level (Double 1.0 - 5.0)\n"
                "  4. estimated_volume_m3 (Double)\n"
                "  5. Add a waste type to waste_type array"
            )
            choice = prompt_str("Choose option (1-5)", default="1")
            if choice == "1":
                update_fields["status"] = prompt_str(
                    "New Status", default="Remediated"
                )
            elif choice == "2":
                update_fields["is_contained"] = prompt_bool(
                    "Is the hazard contained now?", default=True
                )
            elif choice == "3":
                update_fields["hazard_level"] = prompt_float(
                    "New Hazard Level (1.0 - 5.0)",
                    default=3.0,
                    min_val=1.0,
                    max_val=5.0,
                )
            elif choice == "4":
                update_fields["estimated_volume_m3"] = prompt_float(
                    "New Estimated Volume (m3)", default=1.5, min_val=0.01
                )
            elif choice == "5":
                new_waste = prompt_str("Waste type to add", default="lead_batteries")
                res = collection.update_one(
                    {"_id": existing["_id"]},
                    {"$addToSet": {"waste_type": new_waste}},
                )
                print(f"[SUCCESS] Modified {res.modified_count} document(s).")
                updated = collection.find_one({"_id": existing["_id"]})
                if updated:
                    pretty_print_doc(updated)
                return
            else:
                print("[!] Invalid selection.")
                return
        else:
            print(
                "\nSelect field to update in 'patrolInspections':\n"
                "  1. fine_details.payment_status (Unpaid / Paid / Appealed)\n"
                "  2. fine_details.amount_eur (Double)\n"
                "  3. infraction_confirmed (Boolean)\n"
                "  4. cleanup_required (Boolean)\n"
                "  5. dispatch_cleanup_crew.cost_eur (Double)"
            )
            choice = prompt_str("Choose option (1-5)", default="1")
            if choice == "1":
                update_fields["fine_details.payment_status"] = prompt_str(
                    "New Payment Status", default="Paid"
                )
            elif choice == "2":
                update_fields["fine_details.amount_eur"] = prompt_float(
                    "New Fine Amount (EUR)", default=3000.0, min_val=0.0
                )
                update_fields["fine_issued"] = True
            elif choice == "3":
                update_fields["infraction_confirmed"] = prompt_bool(
                    "Is infraction confirmed?", default=True
                )
            elif choice == "4":
                update_fields["cleanup_required"] = prompt_bool(
                    "Is cleanup required?", default=False
                )
            elif choice == "5":
                update_fields["dispatch_cleanup_crew.cost_eur"] = prompt_float(
                    "Updated Cleanup Cost (EUR)", default=2100.0, min_val=0.0
                )
            else:
                print("[!] Invalid selection.")
                return

        res = collection.update_one(
            {"_id": existing["_id"]}, {"$set": update_fields}
        )
        print(
            f"\n[SUCCESS] Matched: {res.matched_count}, "
            f"Modified: {res.modified_count} document(s)."
        )
        updated_doc = collection.find_one({"_id": existing["_id"]})
        if updated_doc:
            print("\nUpdated Document:")
            pretty_print_doc(updated_doc)
    except PyMongoError as exc:
        print(f"[ERROR] Failed to update document: {exc}")

def delete_existing_document(collection: Collection) -> None:
    print(f"\n=== [4] DELETE EXISTING DOCUMENT FROM '{collection.name}' ===")
    key_label = (
        "incident_id (e.g. INC-2026-011)"
        if collection.name == COLLECTION_INCIDENTS
        else "inspection_id (e.g. INS-2026-8811)"
    )
    identifier = prompt_str(f"Enter {key_label} or _id to delete")
    query_filter = build_identifier_filter(collection.name, identifier)

    try:
        existing = collection.find_one(query_filter)
        if not existing:
            print(f"[!] No document found matching '{identifier}'.")
            return

        print("\nDocument found:")
        pretty_print_doc(existing)
        if not prompt_bool(
            "Are you sure you want to permanently delete this document?",
            default=False,
        ):
            print("Deletion cancelled.")
            return

        res = collection.delete_one({"_id": existing["_id"]})
        print(
            f"[SUCCESS] Deleted {res.deleted_count} document(s) from '{collection.name}'."
        )
    except PyMongoError as exc:
        print(f"[ERROR] Failed to delete document: {exc}")

def search_documents(collection: Collection) -> None:
    print(f"\n=== [5] SEARCH DOCUMENTS IN '{collection.name}' ===")
    keyword = prompt_str(
        "Enter search keyword (e.g. district, waste type, status, officer, offender, or ID)"
    )
    escaped = re.escape(keyword)
    regex = {"$regex": escaped, "$options": "i"}

    if collection.name == COLLECTION_INCIDENTS:
        search_filter: Dict[str, Any] = {
            "$or": [
                {"incident_id": regex},
                {"status": regex},
                {"waste_type": regex},
                {"address.street": regex},
                {"address.district": regex},
                {"address.city": regex},
                {"address.postal_code": regex},
                {"citizen_reporter.username": regex},
                {"citizen_reporter.name": regex},
                {"citizen_reporter.citizen_id": regex},
            ]
        }
    else:
        search_filter = {
            "$or": [
                {"inspection_id": regex},
                {"incident_ref": regex},
                {"patrol_officer.badge_id": regex},
                {"patrol_officer.officer_name": regex},
                {"patrol_officer.vehicle_unit": regex},
                {"violations_detected": regex},
                {"fine_details.offender_name": regex},
                {"fine_details.payment_status": regex},
                {"dispatch_cleanup_crew.contractor_name": regex},
            ]
        }

    try:
        matches = list(collection.find(search_filter))
        if not matches:
            print(f"No documents in '{collection.name}' matched keyword '{keyword}'.")
            return

        print(f"\nFound {len(matches)} matching document(s) for '{keyword}':")
        for idx, doc in enumerate(matches, start=1):
            pretty_print_doc(doc, idx)
    except PyMongoError as exc:
        print(f"[ERROR] Search failed: {exc}")