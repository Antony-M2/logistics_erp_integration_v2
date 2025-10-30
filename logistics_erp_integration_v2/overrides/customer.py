import frappe
from erpnext.selling.doctype.customer.customer import Customer
from logistics_erp_integration_v2.utils.duplicate import (
    check_dublicate_value_details, get_child_table_changed_and_newly_added_details
)
from logistics_erp_integration_v2.utils.auto_user_permission import (
    get_previous_company_mapping_details,
    create_or_update_user_permission_for_company
)


class CustomCustomer(Customer):
    
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

        self.create_permission = new_entries + updated_entries
        self.delete_permission = delete_entries

    def on_update(self):
        """
        This method is called when the Customer document is updated & Newly Inserted
        """
        super().on_update()

        if self.create_permission or self.delete_permission:
            # create_or_update_user_permission_for_company(
            #     self.create_permission, self.delete_permission, frappe.session.user
            # )
        
            frappe.enqueue(
                create_or_update_user_permission_for_company,
                queue='default',
                create_permission=self.create_permission,
                delete_permission=self.delete_permission,
                session_user=frappe.session.user
            )