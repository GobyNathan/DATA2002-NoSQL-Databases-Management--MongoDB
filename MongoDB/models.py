from datetime import datetime, timezone
from typing import Any, Dict
from MongoDB.config import VALID_INCIDENT_STATUSES
from MongoDB.utils import prompt_bool, prompt_float, prompt_list, prompt_str

def build_new_incident_doc() -> Dict[str, Any]:
    print("\n--- Enter Hazardous Incident Details ---")
    incident_id = prompt_str("Incident ID (e.g. INC-2026-011)", default="INC-2026-011")
    waste_type = prompt_list(
        "Waste Types", default_list=["asbestos", "industrial_solvents"]
    )
    hazard_level = prompt_float(
        "Hazard Level (1.0 to 5.0)", default=4.0, min_val=1.0, max_val=5.0
    )
    is_contained = prompt_bool("Is the hazard currently contained?", default=False)
    estimated_volume_m3 = prompt_float(
        "Estimated Volume (m3)", default=2.5, min_val=0.01
    )

    print(f"Available statuses: {', '.join(VALID_INCIDENT_STATUSES)}")
    status = prompt_str("Incident Status", default="Open")

    print("\n--- GPS Coordinates (GeoJSON Point - Dublin area defaults) ---")
    longitude = prompt_float(
        "Longitude (-180 to 180)", default=-6.2603, min_val=-180.0, max_val=180.0
    )
    latitude = prompt_float(
        "Latitude (-90 to 90)", default=53.3498, min_val=-90.0, max_val=90.0
    )

    print("\n--- Embedded Address Details ---")
    street = prompt_str("Street", default="Docklands Industrial Quay 14")
    district = prompt_str("City District (e.g. Dublin 1, Dublin 8)", default="Dublin 1")
    city = prompt_str("City", default="Dublin")
    postal_code = prompt_str("Postal Code / Eircode", default="D01 X4W2")

    print("\n--- Embedded Citizen Reporter Details ---")
    is_anonymous = prompt_bool("Is reporter anonymous?", default=False)
    if is_anonymous:
        citizen_id = "ANON"
        username = "anonymous_citizen"
        contact_phone = "N/A"
        verified_reporter = False
    else:
        citizen_id = prompt_str("Citizen ID", default="CIT-409")
        username = prompt_str("Citizen Username / Name", default="ciaran_murphy")
        contact_phone = prompt_str("Contact Phone", default="+353-87-555-0192")
        verified_reporter = prompt_bool("Verified Citizen Account?", default=True)

    return {
        "incident_id": incident_id,
        "reported_date": datetime.now(timezone.utc),
        "waste_type": waste_type,
        "hazard_level": hazard_level,
        "is_contained": is_contained,
        "location": {
            "type": "Point",
            "coordinates": [longitude, latitude],
        },
        "address": {
            "street": street,
            "district": district,
            "city": city,
            "postal_code": postal_code,
        },
        "citizen_reporter": {
            "citizen_id": citizen_id,
            "username": username,
            "contact_phone": contact_phone,
            "is_anonymous": is_anonymous,
            "verified_reporter": verified_reporter,
        },
        "estimated_volume_m3": estimated_volume_m3,
        "status": status,
    }

def build_new_inspection_doc() -> Dict[str, Any]:
    print("\n--- Enter Patrol Inspection Details ---")
    inspection_id = prompt_str(
        "Inspection ID (e.g. INS-2026-8811)", default="INS-2026-8811"
    )
    incident_ref = prompt_str(
        "Referenced Incident ID (incident_ref, e.g. INC-2026-001)",
        default="INC-2026-001",
    )

    print("\n--- Embedded Patrol Officer Details ---")
    badge_id = prompt_str("Officer Badge ID", default="EPA-DUB-204")
    officer_name = prompt_str("Officer Name", default="Aoife O'Connor")
    vehicle_unit = prompt_str("Vehicle Unit", default="HAZ-UNIT-03")

    infraction_confirmed = prompt_bool("Was an infraction confirmed?", default=True)
    violations_detected = (
        prompt_list(
            "Violations Detected",
            default_list=["illegal_spill", "unlicensed_transport"],
        )
        if infraction_confirmed
        else []
    )

    fine_issued = prompt_bool("Was a fine issued?", default=infraction_confirmed)
    if fine_issued:
        print("\n--- Embedded Fine Details ---")
        amount_eur = prompt_float("Fine Amount (EUR)", default=2500.0, min_val=0.0)
        offender_name = prompt_str(
            "Offender / Company Name", default="Liffey Haulage Ltd."
        )
        payment_status = prompt_str(
            "Payment Status (Unpaid / Paid / Appealed)", default="Unpaid"
        )
        fine_details = {
            "amount_eur": amount_eur,
            "offender_name": offender_name,
            "payment_status": payment_status,
        }
    else:
        fine_details = {
            "amount_eur": 0.0,
            "offender_name": "N/A",
            "payment_status": "Not Applicable",
        }

    cleanup_required = prompt_bool("Is specialist cleanup required?", default=True)
    if cleanup_required:
        print("\n--- Embedded Cleanup Crew Dispatch Details ---")
        contractor_name = prompt_str(
            "Contractor Name", default="GreenSafe BioHazard Remediation"
        )
        cost_eur = prompt_float("Cleanup Cost (EUR)", default=1800.0, min_val=0.0)
        collected_weight_kg = prompt_float(
            "Collected Waste Weight (kg)", default=420.0, min_val=0.0
        )
        dispatch_cleanup_crew = {
            "contractor_name": contractor_name,
            "assigned_date": datetime.now(timezone.utc),
            "cost_eur": cost_eur,
            "collected_weight_kg": collected_weight_kg,
        }
    else:
        dispatch_cleanup_crew = {
            "contractor_name": "None",
            "assigned_date": None,
            "cost_eur": 0.0,
            "collected_weight_kg": 0.0,
        }

    print("\n--- Inspection Site GPS Coordinates (GeoJSON Point) ---")
    longitude = prompt_float(
        "Longitude (-180 to 180)", default=-6.2603, min_val=-180.0, max_val=180.0
    )
    latitude = prompt_float(
        "Latitude (-90 to 90)", default=53.3498, min_val=-90.0, max_val=90.0
    )

    return {
        "inspection_id": inspection_id,
        "incident_ref": incident_ref,
        "patrol_officer": {
            "badge_id": badge_id,
            "officer_name": officer_name,
            "vehicle_unit": vehicle_unit,
        },
        "inspection_date": datetime.now(timezone.utc),
        "violations_detected": violations_detected,
        "infraction_confirmed": infraction_confirmed,
        "fine_issued": fine_issued,
        "fine_details": fine_details,
        "cleanup_required": cleanup_required,
        "dispatch_cleanup_crew": dispatch_cleanup_crew,
        "site_coordinates": {
            "type": "Point",
            "coordinates": [longitude, latitude],
        },
    }