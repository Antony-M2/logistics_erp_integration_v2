from erpnext.selling.doctype.customer.customer import Customer
from logistics_erp_integration_v2.utils.duplicate import check_dublicate_value_details
from logistics_erp_integration_v2.utils.auto_user_permission import get_previous_company_mapping_details

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