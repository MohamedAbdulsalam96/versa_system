frappe.ui.form.on("Sales Order", {
  onload: function (frm) {
    if (!frm.doc.delivery_date) {
      // Check if delivery_date is not already set
      // Get today's date
      var today = new Date();
      // Add 10 days to today's date
      today.setDate(today.getDate() + 10);
      // Format the date to YYYY-MM-DD
      var default_date = today.toISOString().split("T")[0];
      // Set the default date in the delivery_date field
      frm.set_value("delivery_date", default_date);
    }
  },

  refresh: function (frm) {
    // Set the indicator label based on the current status
    setStatusIndicator(frm);
  },

  status: function (frm) {
    // Update the indicator label dynamically when the status changes
    setStatusIndicator(frm);
  },
});

// Function to set the indicator label based on status
function setStatusIndicator(frm) {
  if (frm.doc.status === "Proforma Invoice") {
    frm.page.set_indicator("Proforma Invoice", "blue");
  } else if (frm.doc.status === "To Deliver and Bill") {
    frm.page.set_indicator("To Deliver and Bill", "red");
  }
}
