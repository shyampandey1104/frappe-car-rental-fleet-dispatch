# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "carrental"
app_title = "Frappe Car Rental Fleet Dispatch"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Car Rental Fleet Dispatch for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/carrental/css/carrental.bundle.css"
app_include_js = "/assets/carrental/js/carrental.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "carrental.engine.on_document_submit",
        "on_cancel": "carrental.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "carrental.engine.daily_scheduled_sync"
    ]
}
