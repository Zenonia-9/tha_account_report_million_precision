"""Run with: odoo shell -d THA --no-http < validate_million_precision.py"""

report = env.ref("account_reports.profit_and_loss")
value = 1_234_567.0
module = env["ir.module.module"].search([
    ("name", "=", "tha_account_report_million_precision"),
], limit=1)
assert module.state == "installed", module.state

million_options = report.get_options({})
million_options["rounding_unit"] = "millions"
assert million_options["rounding_unit"] == "millions"
million_display = report.format_value(million_options, value, "monetary")
assert million_display == "1.23", million_display

small_million_display = report.format_value(million_options, 1.0, "monetary")
assert small_million_display == "0.00", small_million_display

for rounding_unit in ("decimals", "units", "thousands"):
    options = report.get_options({})
    options["rounding_unit"] = rounding_unit
    assert report.format_value(options, value, "monetary") != million_display

xlsx_options = report.get_options({})
xlsx_options.update({"rounding_unit": "millions", "export_mode": "file"})
xlsx = report.export_to_xlsx(xlsx_options)
assert xlsx.get("file_content"), "Expected a non-empty XLSX export"

print("Million precision validation passed:", million_display, small_million_display)
