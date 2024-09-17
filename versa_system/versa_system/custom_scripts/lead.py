import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
                "field_map": {
    
                    "first_name": "from_lead",              
                    #"custom_material_type": "material"
                },
            },
            "Properties": {                               
                "doctype": "Properties",
                "field_map": {
                    'finishing': 'finishing',             
                    'color': 'color',
                    'material': 'material'
                },
            },
            "Size Chart": {                               
                "doctype": "Size Chart",
                "field_map": {
                    'size': 'size',             
                    'dimensions': 'dimensions',
                    
                },
            },
        }, target_doc)

    return target_doc