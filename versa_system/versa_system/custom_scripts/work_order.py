import frappe

@frappe.whitelist()
def update_sales_order_status_on_work_order_completion(work_order_name):
    """Update the status of the linked Sales Order when Work Order is completed."""
    try:
        frappe.log_error(f"update_sales_order_status_on_work_order_completion called for Work Order: {work_order_name}")
        
        # Fetch the Work Order document
        work_order = frappe.get_doc("Work Order", work_order_name)

        # Ensure Work Order is linked to a Sales Order
        if work_order.sales_order:
            # Fetch the Sales Order document
            sales_order = frappe.get_doc("Sales Order", work_order.sales_order)
            frappe.log_error(f"Work Order Status: {work_order.status}, Sales Order Status: {sales_order.status}")
            
            # Update Sales Order status if Work Order is completed
            if work_order.status == "Completed":
                frappe.db.set_value("Sales Order", sales_order.name, "status", "Proforma Invoice")
                frappe.db.commit()
                frappe.log_error(f"Sales Order status updated to 'Proforma Invoice'.")
                return "Success"
            else:
                frappe.log_error(f"Work Order status is not 'Completed'.")
                return "Work Order is not 'Completed'"
        else:
            frappe.log_error(f"No Sales Order linked to Work Order {work_order_name}.")
            return "No Sales Order linked to Work Order"

    except frappe.DoesNotExistError:
        frappe.log_error(f"Work Order {work_order_name} does not exist.")
        return "Work Order does not exist"
    except Exception as e:
        frappe.log_error(f"Failed to update Sales Order status: {str(e)}")
        return f"Error: {str(e)}"
