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
from novaclient.v1_1.contrib import openclqueues
from novaclient.tests.v1_1.contrib import fakes
from novaclient.tests import utils

extensions = [
    extension.Extension(openclqueues.__name__.split(".")[-1], openclqueues),
    ]

cs = fakes.FakeClient(extensions=extensions)

class OpenclqueuesinterfaceTest(object):

    def test_list_queues(self):
        ocs = cs.openclqueues.list()
        cs.assert_called('GET', '/os-openclqueues')
        print( ocs )

    def test_queue_properties(self):
        queue_id = 0
        ocs = cs.openclqueues.show(queue_id)
        cs.assert_called('GET', '/os-openclqueues/%d' % queue_id)

    def test_queue_create(self):
        device_id = 0
        context_id = 0
        properties = []
        ocs = cs.openclqueues.create(device_id, context_id, properties)
        cs.assert_called('POST', '/os-openclqueues')

    def test_queue_retain(self):
        queue_id = 1
        ocs = cs.openclqueues.retain(queue_id)
        cs.assert_called('POST', '/os-openclqueues/%d/retain' % queue_id)

    def test_queue_release(self):
        queue_id = 1
        ocs = cs.openclqueues.release(queue_id)
        cs.assert_called('POST', '/os-openclqueues/%d/release' % queue_id)

    def test_queue_enqueuereadbuffer(self):
        q_id = 1
        b_id = 1
        bc = 128
        ocs = cs.openclqueues.enqueuereadbuffer(queue_id=q_id, buffer_id=b_id, ByteCount=bc)
        cs.assert_called('POST', '/os-openclqueues/%d/enqueuereadbuffer' % q_id)

    def test_queue_enqueuewritebuffer(self):
        q_id = 1
        b_id = 1
        bc = 128
        dt = 'ABCD123'
        ocs = cs.openclqueues.enqueuewritebuffer(queue_id=q_id, buffer_id=b_id, ByteCount=bc, data=dt)
        cs.assert_called('POST', '/os-openclqueues/%d/enqueuewritebuffer' % q_id)

    def test_queue_enqueuecopybuffer(self):
        q_id = 1
        bs_id = 1
        bd_id = 1
        bc = 128
        ocs = cs.openclqueues.enqueuecopybuffer(queue_id=q_id, source_buffer_id=bs_id, 
                                                destination_buffer_id=bd_id, ByteCount=bc)
        cs.assert_called('POST', '/os-openclqueues/%d/enqueuecopybuffer' % q_id)

    def test_queue_enqueuendrangekernel(self):
        q_id = 1
        k_id = 1
        gwsz = [1,]
        gwo = [0,]
        lwsz = [1,]
        ocs = cs.openclqueues.enqueuendrangekernel(queue_id=q_id, kernel_id=k_id, 
                                                global_size=gwsz, global_offset=gwo, 
                                                local_size=lwsz)
        cs.assert_called('POST', '/os-openclqueues/%d/enqueuendrangekernel' % q_id)

    def test_queue_enqueuetask(self):
        q_id = 1
        k_id = 1
        ocs = cs.openclqueues.enqueuetask(queue_id=q_id, kernel_id=k_id)
        cs.assert_called('POST', '/os-openclqueues/%d/enqueuetask' % q_id)

    def test_queue_enqueuebarrier(self):
        q_id = 1
        ocs = cs.openclqueues.enqueuebarrier(queue_id=q_id)
        cs.assert_called('POST', '/os-openclqueues/%d/enqueuebarrier' % q_id)

    def test_queue_finish(self):
        q_id = 1
        ocs = cs.openclqueues.finish(queue_id=q_id)
        cs.assert_called('POST', '/os-openclqueues/%d/finish' % q_id)

ocltest = OpenclqueuesinterfaceTest()
ocltest.test_list_queues()
ocltest.test_queue_properties()
ocltest.test_queue_create()
ocltest.test_queue_retain()
ocltest.test_queue_release()
ocltest.test_queue_enqueuereadbuffer()
ocltest.test_queue_enqueuewritebuffer()
ocltest.test_queue_enqueuecopybuffer()
ocltest.test_queue_enqueuendrangekernel()
ocltest.test_queue_enqueuetask()
ocltest.test_queue_enqueuebarrier()
ocltest.test_queue_finish()

