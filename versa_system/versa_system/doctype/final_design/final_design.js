frappe.ui.form.on('Final Design', {
    refresh: function(frm) {
        // Check if the workflow state is "Approved"
        if (!frm.is_new() && frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Sales Order'), function() {
                // Call the mapping function for Final Design to Sales Order
                frappe.model.open_mapped_doc({
                    method: 'versa_system.versa_system.doctype.final_design.final_design.map_final_design_to_sales_order',
                    frm: frm
                });
            }, __('Create'));
        }
    }
});
