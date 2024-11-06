import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe import _

def after_install():
    create_custom_fields(get_brand_custom_fields(), ignore_validate=True)
    create_custom_fields(get_quotation_custom_fields(), ignore_validate=True)



def after_migrate():
    after_install()

def before_uninstall():
    delete_custom_fields(get_brand_custom_fields())
    delete_custom_fields(get_quotation_custom_fields())


def delete_custom_fields(custom_fields: dict):
    """
    Method to delete custom fields from doctypes.

    Args:
        custom_fields (dict): Dictionary of custom fields with the format
                              {'Doctype': [{'fieldname': 'your_fieldname', ...}]}
    """
    for doctype, fields in custom_fields.items():
        frappe.db.delete(
            "Custom Field",
            {"fieldname": ("in", [field["fieldname"] for field in fields]), "dt": doctype}
        )
        frappe.clear_cache(doctype=doctype)

def get_brand_custom_fields():
    """
    Define custom fields for the Brand doctype.

    Returns:
        dict: Custom field definitions for the Brand doctype.
    """
    return {
        "Brand": [
            {
                "fieldname": "item",  # Internal fieldname
                "fieldtype": "Link",  # Field type: Link
                "label": "Item",  # Field label
                "options": "Item",  # Link to the Item doctype
                "insert_after": "brand",  # Field location (insert after Brand field)
                "reqd": 1  # Mark the field as mandatory (1 = True, 0 = False)
            }
        ]
    }
def get_quotation_custom_fields():
    """
    Define custom fields for the Quotation doctype.

    Returns:
        dict: Custom field definitions for the Quotation doctype.
    """
    return {
        "Quotation": [
            {
                "fieldname": "final_design_approval",
                "fieldtype": "Data",
                "label": "Final Design Approval",
                "insert_after": "order_type",  
                "reqd": 1
            }
        ]
    }
