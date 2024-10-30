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
        # Add any additional custom assignments here
        target.from_lead = source.party_name

    # Mapping the Quotation to Final Design
    target_doc = get_mapped_doc("Quotation", source_name, {
        "Quotation": {
            "doctype": "Final Design",
            "field_map": {
                "party_name": "from_lead"
            }
        }
    }, target_doc, set_missing_values)

    # Fetching items from the Quotation and appending to 'items' table in Final Design
    quotation_doc = frappe.get_doc("Quotation", source_name)
    for item in quotation_doc.get("items"):
        target_doc.append("quotation_details", {
            "item_code": item.item_code,
            "uom": item.uom,
            "qty": item.qty
        })

    quotation_doc = frappe.get_doc("Quotation", source_name)
    for item in quotation_doc.get("items"):
        target_doc.append("items", {
            "item_code": item.item_code
    })



    return target_doc
