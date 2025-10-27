

frappe.ui.form.on("Customer", {


});



frappe.ui.form.on('LEI Company Mapping', {
    custom_company_add(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        child.company = null;
        frm.refresh_field('custom_company');
    },
    company(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        let isDublicate = checkDuplicateCompanies(frm);
        if (isDublicate) {
            child.company = null;
            frm.refresh_field('custom_company');
        }
    }
});


const checkDuplicateCompanies = (frm) => {
    let companies = frm.doc.custom_company
    let dublicates = []

    for (let company of companies) {
        if (dublicates.includes(company.company)) {
            frappe.msgprint(`Duplicate company found: ${company.company}. Please select a different company.`);
            return true;
        } else {
            if (company.company !== null) {
                dublicates.push(company.company);
            }
        }
    }
    return false;
};

