import copy
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


def get_child_table_changed_and_newly_added_details(previous_data: List[Dict], current_data: list[Dict]) -> tuple[Dict]:
    """
    Check the child table data to identify changed and newly added entries.

    Args:
        previous_data (List[Dict]): The previous state of the child table data.
        current_data (List[Dict]): The current state of the child table data.
    Returns:
        Tuple[Dict]: A tuple containing two dictionaries:
            - changed_entries: Entries that have been modified.
            - newly_added_entries: Entries that are newly added.
    """
    new_entries = [d for d in current_data if d.get("__islocal") and d.get("__unsaved")]

    updated_entries = []
    delete_entries = []
    for curr_entry in current_data:
        if curr_entry.get("__unsaved") and not curr_entry.get("__islocal"):
            for prev_entry in previous_data:
                if curr_entry.get("name") == prev_entry.get("name"):
                    if curr_entry.get("company") != prev_entry.get("company"):
                        updated_entries.append(curr_entry)
                        delete_entries.append(prev_entry)
                    break
    
    # Remove row add same previously deleted
    new_entries_ = copy.deepcopy(new_entries)
    for index, ne in enumerate(new_entries_):
        for prev_entry in previous_data:
            if ne.get("company") == prev_entry.get("company"):
                new_entries.pop(index)
                break
    
    # Switch same values in different rows pretent to be updated
    updated_entries_ = copy.deepcopy(updated_entries)
    for index, ue in enumerate(updated_entries_):
        for prev_entry in previous_data:
            if ue.get("company") == prev_entry.get("company"):
                updated_entries.pop(index)
                delete_entries.remove(prev_entry)
                break
    
    # Delete and add new row different values
    for prev_entry in previous_data:
        is_deleted = True
        for curr_entry in current_data:
            if curr_entry.get("name") == prev_entry.get("name"):
                is_deleted = False
                break
        if is_deleted:
            delete_entries.append(prev_entry)
    
    # Delete row add same values in different rows
    delete_entries_ = copy.deepcopy(delete_entries)
    for index, de in enumerate(delete_entries_):
        for curr_entry in current_data:
            if de.get("company") == curr_entry.get("company"):
                delete_entries.pop(index)
                break

    return new_entries, updated_entries, delete_entries