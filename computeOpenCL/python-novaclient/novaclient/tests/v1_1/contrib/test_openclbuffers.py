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
from novaclient.v1_1.contrib import openclbuffers
from novaclient.tests.v1_1.contrib import fakes
from novaclient.tests import utils

extensions = [
    extension.Extension(openclbuffers.__name__.split(".")[-1], openclbuffers),
    ]

cs = fakes.FakeClient(extensions=extensions)

class OpenclbuffersinterfaceTest(object):

    def test_list_buffers(self):
        ocs = cs.openclbuffers.list()
        cs.assert_called('GET', '/os-openclbuffers')
        print( ocs )

    def test_buffer_properties(self):
        buffer_id = 0
        ocs = cs.openclbuffers.show(buffer_id)
        cs.assert_called('GET', '/os-openclbuffers/%d' % buffer_id)

    def test_buffer_create(self):
        context_id = 0
        MemSize = 128
        properties = []
        ocs = cs.openclbuffers.create(context_id, MemSize, properties)
        cs.assert_called('POST', '/os-openclbuffers')

    def test_buffer_retain(self):
        buffer_id = 1
        ocs = cs.openclbuffers.retain(buffer_id)
        cs.assert_called('POST', '/os-openclbuffers/%d/retain' % buffer_id)

    def test_buffer_release(self):
        buffer_id = 1
        ocs = cs.openclbuffers.release(buffer_id)
        cs.assert_called('POST', '/os-openclbuffers/%d/release' % buffer_id)

ocltest = OpenclbuffersinterfaceTest()
ocltest.test_list_buffers()
ocltest.test_buffer_properties()
ocltest.test_buffer_create()
ocltest.test_buffer_retain()
ocltest.test_buffer_release()

