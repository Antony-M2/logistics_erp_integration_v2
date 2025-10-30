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



def create_or_update_user_permission_for_company(
    create_permission: List[Dict],
    delete_permission: List[Dict],
    session_user: str
):
    """
    Create or update User Permissions for the specified user based on the created and deleted company mappings.

    Args:
        create_permission (List[Dict]): A list of dictionaries containing newly created company mappings.
        delete_permission (List[Dict]): A list of dictionaries containing deleted company mappings.
        session_user (str): to track who is making the changes.
    """
    doctype = 'LEI Company Mapping'
    if create_permission:
        parent = list(set([cp['parent'] for cp in create_permission]))[0]
        parenttype = list(set([cp['parenttype'] for cp in create_permission]))[0]
        # doctype = list(set([cp['doctype'] for cp in create_permission]))[0]
        companies = list(set([cp['company'] for cp in create_permission]))
        processing_data, passing_parenttype = get_user_permisison_processing_data(doctype, parent, parenttype, companies)
        create_user_permission_for_company(processing_data, parent, passing_parenttype )

    if delete_permission:
        parent = list(set([cp['parent'] for cp in delete_permission]))[0]
        parenttype = list(set([cp['parenttype'] for cp in delete_permission]))[0]
        # doctype = list(set([cp['doctype'] for cp in delete_permission]))[0]
        companies = list(set([cp['company'] for cp in delete_permission]))
        processing_data, passing_parenttype = get_user_permisison_processing_data(doctype, parent, parenttype, companies)
        delete_user_permission_for_company(processing_data, parent, passing_parenttype)
    
    frappe.log_error(
        "create_or_update_user_permission_for_company",
        f"User Permission Updated for \ncreate_permission\n{create_permission}\ndelete_permission\n{delete_permission}",
        reference_doctype=parenttype,
        reference_name=parent
    )

def get_user_permisison_processing_data(doctype, parent, parenttype, companies):
    if parenttype == 'Customer':
        passing_parenttype = 'User'
    elif parenttype == 'User':
        passing_parenttype = 'Customer'
    else:
        frappe.log_error("get_user_permisison_processing_data", "Unexpected Parenttype only processing User and Customer")
        raise Exception("Unexpected Parenttype only processing User and Customer")
    
    data = frappe.db.get_all(
        doctype,
        pluck='parent',
        filters={
            'parenttype': passing_parenttype,
            'company': ['in', companies]
        }
    )
    data = list(set(data))
    return data, passing_parenttype


def create_user_permission_for_company(processing_data: List[str], parent: str, passing_parenttype: str):
    """
    Create a User Permission for the specified user and company.

    Args:
        processing_data: List[str] - Data to create the permission
        parent: str - main parent can be User or Customer
        passing_parenttype: str - User or Customer
    """
    for pd in processing_data:
        if passing_parenttype == 'User':
            user = pd
            customer = parent
        elif passing_parenttype == 'Customer':
            user = parent
            customer = pd
        else:
            frappe.log_error("create_user_permission_for_company", f"Got different passing_parrent {passing_parenttype}")
            raise Exception(f"Got different passing_parrent {passing_parenttype}")

        doc = frappe.get_doc({
            'doctype': 'User Permission',
            'user': user,
            'allow': 'Customer',
            'for_value': customer,
            'apply_to_all_doctypes': 1
        })
        doc.insert()
        doc.add_comment('Comment', 'Created By Auto User Permission for Company Mapping')


def delete_user_permission_for_company(processing_data: List[str], parent: str, passing_parenttype: str):
    """
    Remove the User Permission for the specified user and company.

    Args:
        user (str): The user whose permission will be removed.
        company (str): The company for which the permission is removed.
    """
    if passing_parenttype == 'User':
        users = processing_data
        customers = [parent]
    elif passing_parenttype == 'Customer':
        users = [parent]
        customers = processing_data
    frappe.db.delete(
        'User Permission',
        filters={
            'user': ['in', users],
            'for_value': ['in', customers],
            'allow': 'Customer',
            'apply_to_all_doctypes': 1
        }
    )