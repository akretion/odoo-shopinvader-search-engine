# Copyright 2026 Akretion (https://www.akretion.com).
# @author Benoît Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    def write(self, vals):
        res = super().write(vals)
        if any(
            field in vals
            for field in ("filter_attribute_ids", "filter_pim_attribute_ids")
        ):
            self.env["se.index"]._update_shopinvader_filter_config()
        return res
