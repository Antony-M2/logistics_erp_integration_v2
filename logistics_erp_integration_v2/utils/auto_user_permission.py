import frappe
from typing import List, Dict


def get_previous_company_mapping_details(
    doctype: str,
    parent: str,
    parentfield: str,
    parenttype: str
) -> List[Dict]:
    """
    Retrieve the previous company mapping details for a given parent document. Use this for the Child Table Doctype.

    Args:
        doctype (str): The name of the child Doctype to fetch records from.
        parent (str): The parent document name (e.g., User or Customer).
        parentfield (str): The child table field name in the parent document.
        parenttype (str): The parent Doctype name.

    Returns:
        List[Dict]: A list of dictionaries containing the previously mapped company details.
    """
    previous_list = frappe.db.get_all(
        doctype,
        fields=["*"],
        filters={
            "parent": parent,
            "parentfield": parentfield,
            "parenttype": parenttype
        },
        order_by="idx"
    )
    return previous_list
