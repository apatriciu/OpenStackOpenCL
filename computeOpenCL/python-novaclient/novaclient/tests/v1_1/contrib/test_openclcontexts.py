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
from novaclient.v1_1.contrib import openclcontexts
from novaclient.tests.v1_1.contrib import fakes
from novaclient.tests import utils

extensions = [
    extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
    ]

cs = fakes.FakeClient(extensions=extensions)

class OpenclcontextsinterfaceTest(object):

    def test_list_contexts(self):
        ocs = cs.openclcontexts.list()
        cs.assert_called('GET', '/os-openclcontexts')
        print( ocs )

    def test_context_properties(self):
        context_id = 0
        ocs = cs.openclcontexts.show(context_id)
        cs.assert_called('GET', '/os-openclcontexts/%d' % context_id)

    def test_context_create(self):
        devices = [0,]
        properties = []
        ocs = cs.openclcontexts.create(devices, properties)
        cs.assert_called('POST', '/os-openclcontexts')

    def test_context_retain(self):
        context_id = 1
        ocs = cs.openclcontexts.retain(context_id)
        cs.assert_called('POST', '/os-openclcontexts/%d/retain' % context_id)

    def test_context_release(self):
        context_id = 1
        ocs = cs.openclcontexts.release(context_id)
        cs.assert_called('POST', '/os-openclcontexts/%d/release' % context_id)

ocltest = OpenclcontextsinterfaceTest()
ocltest.test_list_contexts()
ocltest.test_context_properties()
ocltest.test_context_create()
ocltest.test_context_retain()
ocltest.test_context_release()

