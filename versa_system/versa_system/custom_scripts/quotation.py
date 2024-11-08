import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_quotation_to_final_design(source_name, target_doc=None):
    """
    Method to map a Quotation to a Final Design document.
    Args:
        source_name: The name of the Quotation document to be mapped.
        target_doc: The target document to which the Quotation should be mapped.
    Returns:
        The newly created Final Design document.
    """
    def set_missing_values(source, target):
        # Set any additional custom values here
        target.from_lead = source.party_name

    # Mapping the Quotation to Final Design
    target_doc = get_mapped_doc("Quotation", source_name, {
        "Quotation": {
            "doctype": "Final Design",
            "field_map": {
                "party_name": "from_lead"
            }
        },
        "Quotation Item": {
            "doctype": "Final",
            "field_map": {
                "item": "item_code"
            }
        }
    }, target_doc, set_missing_values)

    return target_doc


@frappe.whitelist()
def map_quotation_to_sales_order(source_name, target_doc=None):
    """
    Method to map a Final Design to a Sales Order document.
    Args:
        source_name: The name of the quotation document to be mapped.
        target_doc: The target document to which the quotation should be mapped.
    Returns:
        The newly created Sales Order document.
    """
    def set_missing_values(source, target):
        # Set any additional custom values here
        target.customer = source.from_lead  # Example mapping from Final Design to Sales Order

    # Mapping the Final Design to Sales Order
    target_doc = get_mapped_doc("Quotation", source_name, {
        "Quotation": {
            "doctype": "Sales Order",
            "field_map": {
                "party_name": "customer",  # Adjust according to your Sales Order fields
            }
        },
        "Quotation Item": {
            "doctype": "Sales Order Item",
            "field_map": {
                "item_code": "item_code",  # Adjust as needed
                "qty": "qty",  # Add other necessary mappings
            }
        }
    }, target_doc, set_missing_values)

    return target_doc

@frappe.whitelist()
def check_final_design_status(party_name):
    # Fetch the Final Design linked to the given party_name (from_lead)
    final_design = frappe.get_all(
        "Final Design",
        filters={"from_lead": party_name, "workflow_state": "Approved"},
        fields=["name"]
    )

    if final_design:
        return "Approved"
    else:
        return "Not Approved"
