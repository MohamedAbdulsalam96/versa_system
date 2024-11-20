import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class MockupDesign(Document):
    def validate(self):
        # Ensure each row in lead_details table has an image
        self.check_image_field_in_lead_details()

    def on_update(self):
        # Call the function to update lead status when the document is updated
        update_lead_status_on_mockup_design(self)

    def check_image_field_in_lead_details(self):
        """Ensure each row in the Lead Details table has an image before saving."""
        for row in self.get("lead_details"):
            if not row.image:
                frappe.throw(f"Please add an image in row {row.idx} of the Lead Details table.")

def update_lead_status_on_mockup_design(doc):
    """Update the status of the associated lead when the mockup design is approved or rejected."""
    if doc.from_lead:
        try:
            # Fetch the linked lead document
            lead = frappe.get_doc("Lead", doc.from_lead)

            # Update status based on workflow state
            if doc.workflow_state == "Approved":
                lead.status = "Mockup Design Approved"
            elif doc.workflow_state == "Rejected":
                lead.status = "Mockup Design Rejected"
            elif doc.workflow_state == "Review Request":
                lead.status = "On Review"
            else:
                # Optional: You could add an else block for other states if needed
                pass

            # Save the lead document to commit the status change
            lead.save()

            # Display success message
            frappe.msgprint(
                f"Lead {lead.name} status updated to '{lead.status}'.",
                alert=True
            )
        except frappe.DoesNotExistError:
            frappe.throw(f"The lead {doc.from_lead} does not exist.")
        except Exception as e:
            # Log the error for debugging purposes
            frappe.log_error(f"Failed to update lead status: {str(e)}")
            frappe.throw("An error occurred while updating the lead status.")

@frappe.whitelist()
def map_mockup_design_to_quotation(source_name, target_doc=None):
    """
    Map fields from Mockup Design DocType to Quotation DocType.
    """
    def set_missing_values(source, target):
        target.quotation_to = "Mockup Design"
        target.party_name = source.name
        target.customer_name = source.from_lead
    target_doc = get_mapped_doc("Mockup Design", source_name,
        {
            "Mockup Design": {
                "doctype": "Quotation",
                "field_map": {
                    "from_lead": "party_name"
                },
            },
            "Enqury Details": {  # Assuming the child table in Lead is 'lead_items'
                "doctype": "Quotation Item",  # Actual child table DocType is 'Quotation Item'
                "field_map": {
                    "item": "item_name",
                    "item": "item_code",
                     # Map the rate if available
                }
            }
        }, target_doc, set_missing_values)

    return target_doc
