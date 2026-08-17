# -*- coding: utf-8 -*-

from odoo import models


class AccountReport(models.Model):
    _inherit = "account.report"

    def _format_value(self, options, value, figure_type, format_params=None):
        """Use a consistent two-decimal display for monetary millions.

        Odoo's rounding-unit formatter intentionally removes decimals from
        scaled values. Scale the value here and use decimal formatting so the
        shared report formatter retains exactly two decimal places. Other
        units and figure types remain entirely native.
        """
        if (
            figure_type == "monetary"
            and value is not None
            and options.get("rounding_unit") == "millions"
        ):
            return super()._format_value(
                {**options, "rounding_unit": "decimals"},
                value / 1_000_000.0,
                "float",
                {**(format_params or {}), "digits": 2},
            )
        return super()._format_value(options, value, figure_type, format_params)
