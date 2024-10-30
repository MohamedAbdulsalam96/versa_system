frappe.ui.form.on('Final Design', {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Sales Order'), function() {
            }, __('Create'));
        }
    }
});
