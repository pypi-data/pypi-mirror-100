# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=method-required-super
from contextlib import contextmanager

from odoo.addons.base_rest.controllers.main import _PseudoCollection
from odoo.addons.base_rest.tests.common import BaseRestCase
from odoo.addons.component.core import WorkContext
from odoo.addons.component.tests.common import ComponentMixin
from odoo.addons.queue_job.job import Job
from odoo.addons.server_environment import serv_config
from odoo.tests import SavepointCase

from .. import shopinvader_response


class CommonCase(SavepointCase, ComponentMixin):
    AUTH_API_KEY_NAME = "api_key_shopinvader_test"

    @classmethod
    def setUpClass(cls):
        super(CommonCase, cls).setUpClass()
        cls.setUpComponent()
        cls.env = cls.env(context={"lang": "en_US"})
        cls.backend = cls.env.ref("shopinvader.backend_1")
        cls.backend.bind_all_product()
        cls.shopinvader_session = {}
        cls.api_key = "myApiKey"
        cls.auth_api_key_name = cls.AUTH_API_KEY_NAME
        if cls.auth_api_key_name not in serv_config.sections():
            serv_config.add_section(cls.auth_api_key_name)
            serv_config.set(cls.auth_api_key_name, "user", "admin")
            serv_config.set(cls.auth_api_key_name, "key", cls.api_key)
        cls.backend.auth_api_key_name = cls.auth_api_key_name

    @contextmanager
    def work_on_services(self, **params):
        params = params or {}
        if "shopinvader_backend" not in params:
            params["shopinvader_backend"] = self.backend
        if "shopinvader_session" not in params:
            params["shopinvader_session"] = {}
        collection = _PseudoCollection("shopinvader.backend", self.env)
        yield WorkContext(
            model_name="rest.service.registration",
            collection=collection,
            **params
        )

    def _init_job_counter(self):
        self.existing_job = self.env["queue.job"].search([])

    @property
    def created_jobs(self):
        return self.env["queue.job"].search([]) - self.existing_job

    def _check_nbr_job_created(self, nbr):
        self.assertEqual(len(self.created_jobs), nbr)

    def _perform_created_job(self):
        for job in self.created_jobs:
            Job.load(self.env, job.uuid).perform()

    def setUp(self):
        # resolve an inheritance issue (common.SavepointCase does not call
        # super)
        SavepointCase.setUp(self)
        ComponentMixin.setUp(self)

        shopinvader_response.set_testmode(True)

        @self.addCleanup
        def cleanupShopinvaderResponseTestMode():
            shopinvader_response.set_testmode(False)


class ProductCommonCase(CommonCase):
    def setUp(self):
        super(ProductCommonCase, self).setUp()
        self.template = self.env.ref(
            "product.product_product_4_product_template"
        )
        self.variant = self.env.ref("product.product_product_4b")
        self.template.taxes_id = self.env.ref("shopinvader.tax_1")
        self.shopinvader_variants = self.env["shopinvader.variant"].search(
            [
                ("record_id", "in", self.template.product_variant_ids.ids),
                ("backend_id", "=", self.backend.id),
            ]
        )
        self.shopinvader_variant = self.env["shopinvader.variant"].search(
            [
                ("record_id", "=", self.variant.id),
                ("backend_id", "=", self.backend.id),
            ]
        )


class ShopinvaderRestCase(BaseRestCase):
    AUTH_API_KEY_NAME = "api_key_shopinvader_test"
    AUTH_API_KEY_NAME2 = "api_key_shopinvader_test2"

    def setUp(self, *args, **kwargs):
        super(ShopinvaderRestCase, self).setUp(*args, **kwargs)
        self.backend = self.env.ref("shopinvader.backend_1")
        # To ensure multi-backend works correctly, we just have to create
        # a new one on the same company.
        self.backend_copy = self.env.ref("shopinvader.backend_2")
        self.api_key = "myApiKey"
        self.api_key2 = "myApiKey2"
        self.auth_api_key_name = self.AUTH_API_KEY_NAME
        self.auth_api_key_name2 = self.AUTH_API_KEY_NAME2
        if self.auth_api_key_name not in serv_config.sections():
            serv_config.add_section(self.auth_api_key_name)
            serv_config.set(self.auth_api_key_name, "user", "admin")
            serv_config.set(self.auth_api_key_name, "key", self.api_key)
        if self.auth_api_key_name2 not in serv_config.sections():
            serv_config.add_section(self.auth_api_key_name2)
            serv_config.set(self.auth_api_key_name2, "user", "admin")
            serv_config.set(self.auth_api_key_name2, "key", self.api_key2)
        self.backend.auth_api_key_name = self.auth_api_key_name2
