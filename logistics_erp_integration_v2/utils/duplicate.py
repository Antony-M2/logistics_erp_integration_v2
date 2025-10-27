import frappe
from typing import List, Dict


def check_dublicate_value_details(data: List[Dict], key: Dict[str, str]) -> List:
    """
    Checks for duplicate values in a list of dictionaries based on the given key(s)
    and raises a validation error if duplicates are found.

    Args:
        data (List[Dict]): A list of dictionaries containing data to validate.
        key (Dict[str, str]): A mapping of field names to their labels.
            Example: {'company': 'Company', 'dob': 'Date of Birth'}

    Raises:
        frappe.ValidationError: If duplicate values are found for any key.

    Returns:
        List: A list of field names that had duplicate entries (if any).
    """
    duplicate_fields = []

    for field_name, field_label in key.items():
        seen = {}
        duplicates = []

        for entry in data:
            value = entry.get(field_name)
            if value:
                if value in seen:
                    duplicates.append(value)
                else:
                    seen[value] = True

        if duplicates:
            duplicate_fields.append(field_name)
            duplicates_str = ", ".join(set(duplicates))
            frappe.throw(
                f"{field_label}: {duplicates_str} has duplicates in the field `{field_label}`.<br>Please remove duplicates.",
                title="Duplicate Entry Found"
            )

    return duplicate_fields
