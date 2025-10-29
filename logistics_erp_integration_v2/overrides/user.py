from frappe.core.doctype.user.user import User
from logistics_erp_integration_v2.utils.duplicate import (
    check_dublicate_value_details, get_child_table_changed_and_newly_added_details
)
from logistics_erp_integration_v2.utils.auto_user_permission import get_previous_company_mapping_details

class CustomUser(User):
    
    def validate(self):
        super().validate()
        # Custom validation logic can be added here
        previous_company_mapping_details =get_previous_company_mapping_details(
            "LEI Company Mapping",
            self.name,
            "custom_company",
            self.doctype
        )
        compay_details = [company.__dict__ for company in self.custom_company]
        check_dublicate_value_details(
            compay_details,
            {'company': 'Company'}
        )
        new_entries, updated_entries, delete_entries = get_child_table_changed_and_newly_added_details(previous_company_mapping_details, compay_details)