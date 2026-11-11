import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId

from MongoDB.config import COLLECTION_INCIDENTS


def json_serializer(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return str(obj)
    return str(obj)


def pretty_print_doc(doc: Dict[str, Any], index: Optional[int] = None) -> None:
    header = f"--- Document #{index} ---" if index is not None else "--- Document ---"
    print(header)
    print(json.dumps(doc, indent=2, default=json_serializer, ensure_ascii=False))


def prompt_str(label: str, default: Optional[str] = None, required: bool = True) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        val = input(f"{label}{suffix}: ").strip()
        if not val and default is not None:
            return default
        if val or not required:
            return val
        print("  [!] This field is required. Please enter a value.")


def prompt_float(
    label: str,
    default: Optional[float] = None,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> float:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{label}{suffix}: ").strip()
        if not raw and default is not None:
            return float(default)
        try:
            num = float(raw)
            if min_val is not None and num < min_val:
                print(f"  [!] Value must be >= {min_val}.")
                continue
            if max_val is not None and num > max_val:
                print(f"  [!] Value must be <= {max_val}.")
                continue
            return num
        except ValueError:
            print("  [!] Invalid number. Please enter a numeric value (e.g. 3.5).")


def prompt_bool(label: str, default: bool = False) -> bool:
    default_hint = "Y/n" if default else "y/N"
    while True:
        raw = input(f"{label} ({default_hint}): ").strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes", "true", "1"):
            return True
        if raw in ("n", "no", "false", "0"):
            return False
        print("  [!] Please enter 'y' (yes) or 'n' (no).")


def prompt_list(label: str, default_list: Optional[List[str]] = None) -> List[str]:
    default_str = ", ".join(default_list) if default_list else ""
    suffix = f" [{default_str}]" if default_str else ""
    while True:
        raw = input(f"{label} (comma-separated){suffix}: ").strip()
        if not raw and default_list is not None:
            return default_list
        items = [item.strip() for item in raw.split(",") if item.strip()]
        if items:
            return items
        print("  [!] Please enter at least one item.")


def build_identifier_filter(collection_name: str, identifier: str) -> Dict[str, Any]:
    key_field = (
        "incident_id"
        if collection_name == COLLECTION_INCIDENTS
        else "inspection_id"
    )
    conditions: List[Dict[str, Any]] = [{key_field: identifier}]
    if ObjectId.is_valid(identifier):
        conditions.append({"_id": ObjectId(identifier)})
    return {"$or": conditions} if len(conditions) > 1 else conditions[0]
