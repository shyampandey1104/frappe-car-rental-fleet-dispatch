# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "carrental"
app_title = "Frappe Car Rental Fleet Dispatch"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Car Rental Fleet Dispatch - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/carrental/css/carrental.bundle.css"
app_include_js = "/assets/carrental/js/carrental.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Car Rental Fleet Dispatch Entry": {
        "validate": "carrental.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "carrental.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "carrental.tasks.hourly_sync"
    ],
    "daily": [
        "carrental.tasks.daily_reconciliation"
    ],
    "weekly": [
        "carrental.tasks.weekly_digest"
    ]
}
