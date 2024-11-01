import frappe
from frappe import _

def update_lead_from_feasibility_check(doc, method):
    """
    Update the corresponding Lead document when Feasibility Check is updated.
    """
    if doc.from_lead:  # Ensure this field correctly references a Lead document
        lead_doc = frappe.get_doc("Lead", doc.from_lead)

        # Clear existing entries in Lead's child table if necessary
        lead_doc.set("custom_enquiry_details", [])  # Clear existing entries

        # Variable to track if at least one item is approved
        any_item_approved = False

        # Loop through each item in the 'details' child table of Feasibility Check
        for item in doc.details:
            # Check if the 'approve' checkbox is checked
            if item.approve:
                any_item_approved = True  # At least one item is approved

            # Append new item to Lead's child table
            lead_doc.append("custom_enquiry_details", {
                "item": item.item,
                "brand": item.brand,
                "rate_range": item.rate_range,
                "design": item.design,
                "model": item.model,
                "size": item.size,
                "colour": item.colour,
                "material": item.material,
                "made_machinehand": item.made_machinehand,
                "image": item.image,
                "approve": item.approve
            })

        # Validate that at least one item is approved
        if not any_item_approved:
            frappe.throw(_("At least one item must be approved."))

        # Save the updated Lead document
        try:
            lead_doc.save()
            frappe.msgprint(_("Lead updated successfully."))
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Error Updating Lead")
            frappe.throw(_("An error occurred while updating the Lead: {0}").format(str(e)))
