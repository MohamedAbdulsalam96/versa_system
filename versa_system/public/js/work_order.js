frappe.ui.form.on("Work Order", {
  onload: function (frm) {
    // Add the custom button only if the Sales Order is linked
    if (frm.doc.sales_order && frm.doc.status === "Completed") {
      updateAndNavigateToSalesOrder(frm);
    }
  },

  // Triggered when the status is updated or any changes occur
  status: function (frm) {
    // Add the button if the status is 'Completed'
    if (frm.doc.status === "Completed") {
      updateAndNavigateToSalesOrder(frm);
    } else {
      frm.remove_custom_button(__("Go to Sales Order"));
    }
  },
});

// Function to add button and navigate to Sales Order form
function updateAndNavigateToSalesOrder(frm) {
  // Add a custom button to navigate to the Sales Order form
  frm.add_custom_button(
    __("Go to Sales Order"), // Button label
    function () {
      if (!frm.doc.sales_order) {
        frappe.msgprint(__("Please select a Sales Order before proceeding."));
        return;
      }

      // Update the Sales Order status to "Proforma Invoice"
      frappe.call({
        method:
          "versa_system.versa_system.custom_scripts.work_order.update_sales_order_status_on_work_order_completion",
        args: {
          work_order_name: frm.doc.name,
        },
        callback: function (response) {
          if (response.message === "Success") {
            frappe.msgprint(
              __("Sales Order status updated to 'Proforma Invoice'.")
            );
            // Navigate to the Sales Order form using the linked Sales Order
            frappe.set_route("Form", "Sales Order", frm.doc.sales_order);
          } else {
            frappe.msgprint(__("Error: ") + response.message);
          }
        },
        error: function (error) {
          frappe.msgprint(
            __("Error occurred while updating the Sales Order: ") +
              error.message
          );
        },
      });
    },
    __("Create") // Button group (default is "Create" group)
  );
}
