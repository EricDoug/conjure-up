#!/usr/bin/env python
#
# tests controllers/deploystatus/tui.py
#
# Copyright 2016 Canonical, Ltd.


import unittest
#  from unittest.mock import ANY, call, MagicMock, patch, sentinel
from unittest.mock import MagicMock, patch

from conjureup.controllers.deploystatus.tui import DeployStatusController

from .helpers import test_loop


class DeployStatusTUIRenderTestCase(unittest.TestCase):

    def setUp(self):

        self.utils_patcher = patch(
            'conjureup.controllers.deploystatus.tui.utils')
        self.mock_utils = self.utils_patcher.start()

        self.finish_patcher = patch(
            'conjureup.controllers.deploystatus.tui.'
            'DeployStatusController.finish')
        self.mock_finish = self.finish_patcher.start()

        self.app_patcher = patch(
            'conjureup.controllers.deploystatus.tui.app')
        mock_app = self.app_patcher.start()
        mock_app.ui = MagicMock(name="app.ui")

        self.controller = DeployStatusController()

    def tearDown(self):
        self.utils_patcher.stop()
        self.finish_patcher.stop()
        self.app_patcher.stop()

    def test_render(self):
        "call render"
        self.controller.render()


class DeployStatusTUIFinishTestCase(unittest.TestCase):

    def setUp(self):

        self.controllers_patcher = patch(
            'conjureup.controllers.deploystatus.tui.controllers')
        self.mock_controllers = self.controllers_patcher.start()

        self.utils_patcher = patch(
            'conjureup.controllers.deploystatus.tui.utils')
        self.mock_utils = self.utils_patcher.start()

        self.common_patcher = patch(
            'conjureup.controllers.deploystatus.tui.common')
        self.mock_common = self.common_patcher.start()

        self.render_patcher = patch(
            'conjureup.controllers.deploystatus.tui.'
            'DeployStatusController.render')
        self.mock_render = self.render_patcher.start()
        self.app_patcher = patch(
            'conjureup.controllers.deploystatus.tui.app')
        self.mock_app = self.app_patcher.start()
        self.mock_app.ui = MagicMock(name="app.ui")

        self.controller = DeployStatusController()

    def tearDown(self):
        self.controllers_patcher.stop()
        self.utils_patcher.stop()
        self.render_patcher.stop()
        self.app_patcher.stop()

    def test_finish_ok(self):
        "finish calls steps"
        async def dummy():
            pass

        self.mock_common.wait_for_applications.return_value = dummy()
        with test_loop() as loop:
            loop.run_until_complete(self.controller.finish())
        self.mock_controllers.use.assert_called_once_with('steps')
