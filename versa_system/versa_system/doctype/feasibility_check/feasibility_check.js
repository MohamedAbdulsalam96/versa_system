frappe.ui.form.on("Feasibility Check", {
  refresh: function (frm) {
    // Check if the Feasibility Check is not new and is approved
    if (frm.doc.workflow_state === "Approved") {
      frm.add_custom_button(__("Mockup Design"), function () {
        frappe.model.open_mapped_doc({
          method:
            "versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_feasibility_to_mockup_design",
          frm: frm,
        });
      });

      // Call the function to update the Lead and add the navigation button
      updateAndNavigateToLead(frm);
    }
  },

  after_save: function (frm) {
    // Check if the current status is 'Lead' and update to 'Interest'
    if (frm.doc.status === "Lead") {
      frm.set_value("status", "Interest");
      frm.save(); // Save again to persist the change
    }
  },

  approve: function (frm) {
    // Approve the feasibility and update lead status if linked
    if (frm.doc.is_approved) {
      frm.set_value("status", "Feasibility Approved"); // Set feasibility status

      if (frm.doc.from_lead) {
        frappe.call({
          method: "frappe.client.set_value",
          args: {
            doctype: "Lead",
            name: frm.doc.from_lead,
            fieldname: "status",
            value: "Feasibility Check Approved",
          },
          callback: function (response) {
            if (response && !response.exc) {
              frappe.msgprint(
                `Lead ${frm.doc.from_lead} status updated to 'Feasibility Check Approved'.`,
                "Status Updated"
              );
            } else {
              frappe.msgprint(__("Failed to update Lead status."));
            }
          },
        });
      }

      frm.save(); // Save the feasibility document after approval
    }
  },

  reject: function (frm) {
    // Reject the feasibility and update lead status if linked
    frm.set_value("status", "Feasibility Rejected"); // Adjust rejection status

    if (frm.doc.from_lead) {
      frappe.call({
        method: "frappe.client.set_value",
        args: {
          doctype: "Lead",
          name: frm.doc.from_lead,
          fieldname: "status",
          value: "Feasibility Check Rejected", // Set lead status to rejected
        },
        callback: function (response) {
          if (response && !response.exc) {
            frappe.msgprint(
              `Lead ${frm.doc.from_lead} status updated to 'Feasibility Check Rejected'.`,
              "Status Updated"
            );
          } else {
            frappe.msgprint(__("Failed to update Lead status."));
          }
        },
      });
    }

    frm.save(); // Save the document to persist the rejection
  },
});

// Function to update the Lead with table data from Feasibility Check
function update_lead_from_feasibility_check(frm) {
  const details = frm.doc.details.map((row) => ({
    item: row.item,
    brand: row.brand,
    rate_range: row.rate_range,
    design: row.design,
    model: row.model,
    approve: row.approve,
  }));

  let messageDisplayed = false;

  frappe.call({
    method: "versa_system.versa_system.custom_scripts.fesibility.update_lead",
    args: {
      lead_name: frm.doc.from_lead,
      details: JSON.stringify(details), // Ensure details are sent as JSON string
    },
    callback: function (response) {
      if (response.message && !messageDisplayed) {
        frappe.msgprint(__("Lead updated successfully."));
        messageDisplayed = true; // Set flag to true after displaying the message
      } else if (!response.message && !messageDisplayed) {
        frappe.msgprint(__("Error occurred while updating the Lead."));
        messageDisplayed = true;
      }
    },
    error: function (error) {
      if (!messageDisplayed) {
        frappe.msgprint(
          __("Error occurred while updating the Lead: ") + error.message
        );
        messageDisplayed = true;
      }
    },
  });
}

// Function to update the Lead and navigate to it
function updateAndNavigateToLead(frm) {
  update_lead_from_feasibility_check(frm);

  // Add a button to navigate to the Lead
  frm.add_custom_button(__("Go to Lead"), function () {
    if (!frm.doc.from_lead) {
      frappe.msgprint(__("Please select a Lead before proceeding."));
      return;
    }
    frappe.set_route("Form", "Lead", frm.doc.from_lead);
  });
}
