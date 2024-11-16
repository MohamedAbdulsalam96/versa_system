import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe import _

def after_install():
    create_custom_fields(get_brand_custom_fields(), ignore_validate=True)
    create_custom_fields(get_quotation_custom_fields(), ignore_validate=True)
    create_property_setters(get_property_setters())

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
                "reqd": 0,
                "allow_on_submit": 1
            }
        ]
    }

def get_property_setters():
    """
    Define specific property setters that need to be added to the Sales Order DocType only.
    """
    return [
        {
            "doctype_or_field": "DocField",
            "doc_type": "Sales Order",
            "field_name": "status",
            "property": "options",
            "value": "Draft\nOn Hold\nTo Deliver and Bill\nTo Bill\nTo Deliver\nCompleted\nCancelled\nClosed\nProforma Invoice"
        },
        {
            "doctype_or_field": "DocField",
            "doc_type": "Sales Order",
            "field_name": "status",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": 1
        }
    ]

def create_property_setters(property_setter_datas):
    """
    Method to create custom property setters.

    Args:
        property_setter_datas: list of dicts for property setter objects
    """
    for data in property_setter_datas:
        # Check for existing property setter based on relevant fields
        if frappe.db.exists("Property Setter", {
            "doc_type": data["doc_type"],
            "field_name": data["field_name"],
            "property": data["property"]
        }):
            continue

        try:
            property_setter = frappe.new_doc("Property Setter")
            property_setter.update(data)
            property_setter.flags.ignore_permissions = True
            property_setter.insert()
        except Exception as e:
            frappe.log_error(f"Error creating property setter for {data['doc_type']} - {data['field_name']}: {str(e)}")
def get_property_setters():
    """
    Define specific property setters that need to be added to the Sales Order DocType only.
    """
    return [
        {
            "doctype_or_field": "DocField",
            "doc_type": "Lead",
            "field_name": "status",
            "property": "options",
            "value": "Lead\n Open\nQuotation\nLost Quotation\nInterested\nFeasibility Check Approved\nConverted\nFeasibility Check Rejected\nMockup Design Approved\nMockup Design Rejected\nOn Review\nQuotation Rejected"
        },
       
    ]
