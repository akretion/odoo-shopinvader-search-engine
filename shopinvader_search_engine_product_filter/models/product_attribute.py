# Copyright 2026 Akretion (https://www.akretion.com).
# @author Benoît Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    def write(self, vals):
        res = super().write(vals)
        if {"is_filterable", "display_type", "name"} & set(vals):
            self.env["se.index"]._update_shopinvader_filter_config()
        return res
