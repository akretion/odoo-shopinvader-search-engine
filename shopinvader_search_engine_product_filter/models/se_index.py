# Copyright 2026 Akretion (https://www.akretion.com).
# @author Benoît Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SeIndex(models.Model):
    _inherit = "se.index"

    def _get_shopinvader_category_indexes(self):
        """Category indexes: the ones indexed on product.category."""
        return self.search([("model_id.model", "=", "product.category")])

    @staticmethod
    def _get_shopinvader_filter_field(attribute):
        """Field description pushed to the search engine configuration."""
        return {
            "name": attribute._get_shopinvader_filter_key(),
            "type": attribute._get_shopinvader_filter_type(),
            "facet": True,
            "optional": True,
            "index": True,
            "sort": False,
            "infix": False,
            "locale": "",
            "stem": False,
            "stem_dictionary": "",
            "store": True,
            "truncate_len": 100,
        }

    def _get_shopinvader_filter_attributes(self):
        """Attributes to expose as filters on this category index.

        Union of the attributes selected on the categories and the default
        filters of the sale channels.
        """
        self.ensure_one()
        categories = self.env["product.category"].search(
            [
                "|",
                ("filter_attribute_ids", "!=", False),
                ("filter_pim_attribute_ids", "!=", False),
            ]
        )
        channels = self.env["sale.channel"].search(
            [
                "|",
                ("filter_attribute_ids", "!=", False),
                ("filter_pim_attribute_ids", "!=", False),
            ]
        )
        owners = list(categories) + list(channels)
        result = []
        seen = set()
        for owner in owners:
            for attribute in owner._get_shopinvader_filters():
                key = attribute._get_shopinvader_filter_key()
                if key and key not in seen:
                    seen.add(key)
                    result.append(attribute)
        return result

    def _update_shopinvader_filter_config(self):
        """Refresh the filter fields of the category indexes.

        The filter fields are rebuilt from the selected attributes; the ones
        previously pushed are replaced, the other fields are kept.
        """
        for index in self._get_shopinvader_category_indexes():
            fields = [
                index._get_shopinvader_filter_field(attribute)
                for attribute in index._get_shopinvader_filter_attributes()
            ]
            names = {field["name"] for field in fields}
            body = dict(index.config_id.body or {})
            kept = [
                field
                for field in body.get("fields", [])
                if field.get("name") not in names
            ]
            body["fields"] = kept + fields
            index.config_id.write({"body": body})
