frappe.ui.form.on('Mockup Design', {
    refresh: function (frm) {
        // Ensure the form is saved before adding buttons
        if (!frm.is_new()) {
            // Add a custom button to navigate to the linked Lead
            if (frm.doc.from_lead) {
                frm.add_custom_button(__('Go to Lead'), function () {
                    frappe.set_route('Form', 'Lead', frm.doc.from_lead);
                });
            }
        }

        // Add a 'Quotation' button if the workflow state is 'Approved'
        if (frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Quotation'), function () {
                frappe.model.open_mapped_doc({
                    method: 'versa_system.versa_system.doctype.mockup_design.mockup_design.map_mockup_design_to_quotation',
                    frm: frm
                });
            }, __('Create'));
        }
    }  
});
