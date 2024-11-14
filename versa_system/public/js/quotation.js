frappe.ui.form.on("Quotation", {
    refresh: function(frm) {
        // Initial Setup: Show "Final Design" button if the Quotation is approved.
        frm.remove_custom_button(__("Sales Order"), "Create");

        if (!frm.is_new() && frm.doc.workflow_state === "Approved") {
            add_final_design_button(frm); // Add Final Design button
            // Check Final Design status after some delay
            setTimeout(function() {
                check_final_design_status_and_update_buttons(frm);
            }, 100); // Adjust the timeout as needed
        }else {
            // Hide the "Create" button if the Quotation is not approved
            frm.page.hide_menu_item("Create");
        }
    },
});

// Function to add the "Final Design" button
function add_final_design_button(frm) {
    frm.add_custom_button(
        __("Final Design"),
        function () {
            frappe.model.open_mapped_doc({
                method: "versa_system.versa_system.custom_scripts.quotation.map_quotation_to_final_design",
                frm: frm,
            });
        },
        __("Create")
    );
}


// Function to add the "Sales Order" button
function add_sales_order_button(frm) {
    frm.add_custom_button(
        __("Sales Order"),
        function () {
            frm.save().then(() => { // Ensure the Quotation is saved
                frappe.model.open_mapped_doc({
                    method: "versa_system.versa_system.custom_scripts.quotation.map_quotation_to_sales_order",
                    frm: frm,
                });
            });
        },
        __("Create")
    );
}

// Function to check the approval status of the associated Final Design and update buttons accordingly
function check_final_design_status_and_update_buttons(frm) {
    const party_name = frm.doc.party_name; // This is mapped to 'from_lead' in Final Design

    if (party_name) {
        // Make an API call to check the Final Design approval status
        frappe.call({
            method: "versa_system.versa_system.custom_scripts.quotation.check_final_design_status",
            args: {
                party_name: party_name, // Send 'party_name' which maps to 'from_lead'
            },
            callback: function (response) {
                if (response.message === "Approved") {
                    // Set the Final Design Status field to 'Approved'
                    frm.set_value('final_design_approval', 'Approved'); // Replace with the actual field name

                    // If Final Design is approved, remove the "Final Design" button and add "Sales Order" button
                    frm.remove_custom_button(__("Final Design"), "Create");
                    add_sales_order_button(frm);
                    console.log("Final Design is approved. Sales Order button is now shown.");
                } else {
                    // Set the Final Design Status field to 'Not Approved'
                    frm.set_value('final_design_approval', 'Not Approved'); // Replace with the actual field name

                    // If Final Design is not approved, remove the "Sales Order" button and add the "Final Design" button
                    frm.remove_custom_button(__("Sales Order"), "Create");
                    add_final_design_button(frm);
                    console.log("Final Design is not approved.");
                }
            },
            error: function (error) {
                console.error("Error checking Final Design status:", error);
            }
        });
    } else {
        console.log("No party_name (from_lead) found.");
    }
}
