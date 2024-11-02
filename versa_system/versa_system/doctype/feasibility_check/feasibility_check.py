import frappe
from frappe.model.document import Document
from frappe import _
from frappe.model.mapper import get_mapped_doc

class FeasibilityCheck(Document):
    pass

@frappe.whitelist()
def map_feasibility_to_mockup_design(source_name, target_doc=None):
    """
    Map fields from Feasibility Check DocType to Mockup Design DocType,
    including only approved rows from the 'Enquiry Details' child table.
    """
    def set_missing_values(source, target):
        # Set any additional values for the target if needed
        pass

    def filter_approved_items(source, target, source_parent):
        # Only map rows where the 'approve' checkbox is checked
        if source.approve:
            target.item = source.item
            target.brand = source.brand
            target.rate_range = source.rate_range
            target.design = source.design
            target.model = source.model
            target.size = source.size
            target.colour = source.colour
            target.material = source.material
            target.made_machinehand = source.made_machinehand
            target.image = source.image

    # Map Feasibility Check to Mockup Design, applying the filter to child table rows
    target_doc = get_mapped_doc(
        "Feasibility Check",
        source_name,
        {
            "Feasibility Check": {
                "doctype": "Mockup Design",
                "field_map": {}
            },
            "Enqury Details": {  # Ensure this matches the target child table name
                "doctype": "Enqury Details",  # Corrected spelling
                "postprocess": filter_approved_items,  # Process only approved items
                "condition": lambda doc: doc.approve  # Only map rows where 'approve' is checked
            }
        },
        target_doc,
        set_missing_values
    )

    return target_doc


def update_lead_status_on_feasibility_check(doc):
    """Update the status of the associated lead when the feasibility check is approved or rejected."""
    if doc.from_lead:
        try:
            # Fetch the linked lead document
            lead = frappe.get_doc("Lead", doc.from_lead)
            
            # Update status based on workflow state
            if doc.workflow_state == "Approved":
                lead.status = "Feasibility Check Approved"
            elif doc.workflow_state == "Rejected":
                lead.status = "Feasibility Check Rejected"
            
            lead.save()

            # Display success message
            frappe.msgprint(
                f"Lead {lead.name} status updated to '{lead.status}'.",
                alert=True
            )
        except frappe.DoesNotExistError:
            frappe.throw(f"The lead {doc.from_lead} does not exist.")
        except Exception as e:
            frappe.log_error(f"Failed to update lead status: {str(e)}")
            frappe.throw("An error occurred while updating the lead status.")
