# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 IBM Corp.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from novaclient import extension
from novaclient.v1_1.contrib import opencldevices
from novaclient.tests.v1_1.contrib import fakes
from novaclient.tests import utils

extensions = [
    extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
    ]

cs = fakes.FakeClient(extensions=extensions)

class OpencldevicesinterfaceTest(object):

    def test_list_devices(self):
        ocs = cs.opencldevices.list()
        cs.assert_called('GET', '/os-opencldevices')
        print( ocs )

    def test_device_properties(self):
        device_id = 0
        ocs = cs.opencldevices.show(device_id)
        cs.assert_called('GET', '/os-opencldevices/%d' % device_id)

ocltest = OpencldevicesinterfaceTest()
ocltest.test_list_devices()
ocltest.test_device_properties()

