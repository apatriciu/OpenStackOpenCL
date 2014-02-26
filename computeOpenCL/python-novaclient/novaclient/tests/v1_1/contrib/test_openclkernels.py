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
from novaclient.v1_1.contrib import openclkernels
from novaclient.tests.v1_1.contrib import fakes
from novaclient.tests import utils

extensions = [
    extension.Extension(openclkernels.__name__.split(".")[-1], openclkernels),
    ]

cs = fakes.FakeClient(extensions=extensions)

class OpenclkernelsinterfaceTest(object):

    def test_list_kernels(self):
        ocs = cs.openclkernels.list()
        cs.assert_called('GET', '/os-openclkernels')
        print( ocs )

    def test_kernel_properties(self):
        kernel_id = 0
        ocs = cs.openclkernels.show(kernel_id)
        cs.assert_called('GET', '/os-openclkernels/%d' % kernel_id)

    def test_kernel_create(self):
        program_id = 0
        KernelName = 'TestKernel'
        ocs = cs.openclkernels.create(program_id, KernelName)
        cs.assert_called('POST', '/os-openclkernels')

    def test_kernel_retain(self):
        kernel_id = 1
        ocs = cs.openclkernels.retain(kernel_id)
        cs.assert_called('POST', '/os-openclkernels/%d/retain' % kernel_id)

    def test_kernel_release(self):
        kernel_id = 1
        ocs = cs.openclkernels.release(kernel_id)
        cs.assert_called('POST', '/os-openclkernels/%d/release' % kernel_id)

    def test_kernel_setkernelarg(self):
        kernel_id = 1
        arg_index = 0
        arg_type = 'SharedMemory'
        arg_value = 128
        ocs = cs.openclkernels.setkernelarg(kernel_id, arg_index, arg_type, arg_value)
        cs.assert_called('POST', '/os-openclkernels/%d/setkernelarg' % kernel_id)

ocltest = OpenclkernelsinterfaceTest()

ocltest.test_list_kernels()
ocltest.test_kernel_properties()
ocltest.test_kernel_create()
ocltest.test_kernel_retain()
ocltest.test_kernel_release()
ocltest.test_kernel_setkernelarg()

