import frappe
from frappe.custom.doctype.customize_form.customize_form import CustomizeForm
from frappe.model import core_doctypes_list, no_value_fields
import copy

class CustomCustomizeForm(CustomizeForm):

    def validate_doctype(self, meta):
        """
        Check if the doctype is allowed to be customized.
        """
        core_doctypes_list_ = copy.deepcopy(core_doctypes_list)
        core_doctypes_list_.remove("User")
        if self.doc_type in core_doctypes_list_:
            frappe.throw(_("Core DocTypes cannot be customized."))

        if meta.issingle:
            frappe.throw(_("Single DocTypes cannot be customized."))

        if meta.custom:
            frappe.throw(_("Only standard DocTypes are allowed to be customized from Customize Form."))