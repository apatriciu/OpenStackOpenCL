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
from novaclient.v1_1.contrib import openclprograms
from novaclient.tests.v1_1.contrib import fakes
from novaclient.tests import utils

extensions = [
    extension.Extension(openclprograms.__name__.split(".")[-1], openclprograms),
    ]

cs = fakes.FakeClient(extensions=extensions)

class OpenclprogramsinterfaceTest(object):

    def test_list_programs(self):
        ocs = cs.openclprograms.list()
        cs.assert_called('GET', '/os-openclprograms')
        print( ocs )

    def test_program_properties(self):
        program_id = 0
        ocs = cs.openclprograms.show(program_id)
        cs.assert_called('GET', '/os-openclprograms/%d' % program_id)

    def test_program_create(self):
        context_id = 0
        ProgramCode = ['',]
        ocs = cs.openclprograms.create(context_id, ProgramCode)
        cs.assert_called('POST', '/os-openclprograms')

    def test_program_retain(self):
        program_id = 1
        ocs = cs.openclprograms.retain(program_id)
        cs.assert_called('POST', '/os-openclprograms/%d/retain' % program_id)

    def test_program_release(self):
        program_id = 1
        ocs = cs.openclprograms.release(program_id)
        cs.assert_called('POST', '/os-openclprograms/%d/release' % program_id)

    def test_program_build(self):
        program_id = 1
        device_id = 1
        build_options = ""
        ocs = cs.openclprograms.build(program_id, [device_id,], build_options)
        cs.assert_called('POST', '/os-openclprograms/%d/build' % program_id)

    def test_program_buildinfo(self):
        program_id = 1
        device_id = 1
        ParamName = 'CL_PROGRAM_BUILD_STATUS'
        ocs = cs.openclprograms.buildinfo(program_id, device_id, ParamName)
        cs.assert_called('POST', '/os-openclprograms/%d/buildinfo' % program_id)


ocltest = OpenclprogramsinterfaceTest()
ocltest.test_list_programs()
ocltest.test_program_properties()
ocltest.test_program_create()
ocltest.test_program_retain()
ocltest.test_program_release()
ocltest.test_program_build()
ocltest.test_program_buildinfo()

