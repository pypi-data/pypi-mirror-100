# Copyright 2020 Camptocamp (http://www.camptocamp.com)
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import os

from odoo.addons.shopinvader_image.tests.common import TestShopinvaderImageCase


class TestShopinvaderImportImageCase(TestShopinvaderImageCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.storage_backend = cls.env.ref(
            "storage_backend.default_storage_backend"
        )
        cls.base_path = os.path.dirname(os.path.abspath(__file__))
        cls.file_csv_content = cls._get_file_content(
            "image_import_test.csv", base_path=cls.base_path
        )
        cls.file_zip_content = cls._get_file_content(
            "image_import_test.zip", base_path=cls.base_path
        )

        cls.wiz = cls._get_wizard(cls)
        cls.products = cls.env["product.template"].search([], limit=2)
        cls.products[0].write({"default_code": "A001", "image_ids": False})
        cls.products[1].write({"default_code": "A002", "image_ids": False})

    def _get_wizard(self, **kw):
        vals = {
            "storage_backend_id": self.storage_backend.id,
            "product_model": "product.template",
            "file_csv": self.file_csv_content,
            "file_zip": self.file_zip_content,
        }
        vals.update(kw)
        return self.env["shopinvader.import.product_image"].create(vals)


class TestShopinvaderImportImage(TestShopinvaderImportImageCase):
    def test_get_lines(self):
        lines = self.wiz._get_lines()
        expected = [
            {
                "default_code": "A00%d" % x,
                "tag_name": "A00%d tag" % x,
                "file_path": "A00%d.jpg" % x,
            }
            for x in range(1, 4)
        ]
        self.assertEqual(lines, expected)

    def test_read_from_zip(self):
        img_content = self._get_file_content(
            "A001.jpg", base_path=self.base_path, as_binary=True
        )
        self.assertEqual(self.wiz._read_from_zip("A001.jpg"), img_content)

    def test_get_b64(self):
        img_content = self._get_file_content(
            "A001.jpg", base_path=self.base_path, as_binary=True
        )
        self.assertEqual(
            self.wiz._get_base64("A001.jpg"),
            ("image/jpeg", base64.encodestring(img_content)),
        )

    def test_import_errors(self):
        self.products[0].default_code = "NONE"
        self.products[1].default_code = "NONE"
        self.wiz.do_import()
        self.assertEqual(
            self.wiz.report,
            {
                "created": [],
                "missing": ["A001", "A002", "A003"],
                "missing_tags": ["A001 tag", "A002 tag", "A003 tag"],
            },
        )

    def test_import_no_overwrite(self):
        self.wiz.do_import()
        self.assertEqual(
            self.wiz.report,
            {
                "created": ["A001", "A002"],
                "missing": ["A003"],
                "missing_tags": ["A001 tag", "A002 tag", "A003 tag"],
            },
        )
        self.assertEqual(len(self.products[0].image_ids), 1)
        self.assertEqual(len(self.products[1].image_ids), 1)
        self.assertFalse(self.products[0].image_ids[0].tag_id)
        self.assertFalse(self.products[1].image_ids[0].tag_id)

        self.wiz.do_import()
        self.assertEqual(
            self.wiz.report,
            {
                "created": ["A001", "A002"],
                "missing": ["A003"],
                "missing_tags": ["A001 tag", "A002 tag", "A003 tag"],
            },
        )
        self.assertEqual(len(self.products[0].image_ids), 2)
        self.assertEqual(len(self.products[1].image_ids), 2)

    def test_import_overwrite(self):
        self.wiz.overwrite = True
        self.wiz.do_import()
        self.assertEqual(
            self.wiz.report,
            {
                "created": ["A001", "A002"],
                "missing": ["A003"],
                "missing_tags": ["A001 tag", "A002 tag", "A003 tag"],
            },
        )
        self.assertEqual(len(self.products[0].image_ids), 1)
        self.assertEqual(len(self.products[1].image_ids), 1)
        self.wiz.do_import()
        self.assertEqual(
            self.wiz.report,
            {
                "created": ["A001", "A002"],
                "missing": ["A003"],
                "missing_tags": ["A001 tag", "A002 tag", "A003 tag"],
            },
        )
        self.assertEqual(len(self.products[0].image_ids), 1)
        self.assertEqual(len(self.products[1].image_ids), 1)

    def test_import_create_missing_tags(self):
        self.wiz.overwrite = True
        self.wiz.create_missing_tags = True
        self.wiz.do_import()
        self.assertEqual(
            self.wiz.report, {"created": ["A001", "A002"], "missing": ["A003"]}
        )
        self.assertEqual(len(self.products[0].image_ids), 1)
        self.assertEqual(len(self.products[1].image_ids), 1)
        self.assertEqual(self.products[0].image_ids[0].tag_id.name, "A001 tag")
        self.assertEqual(self.products[1].image_ids[0].tag_id.name, "A002 tag")
