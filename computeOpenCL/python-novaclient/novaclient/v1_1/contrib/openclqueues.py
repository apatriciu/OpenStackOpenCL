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

"""
openclqueues interface
"""

from novaclient import base
import binascii

class OpenCLQueue(base.Resource):
    def __repr__(self):
        return "<OpenCL Queue: %d>" % self.id

class OpenCLQueueId(base.Resource):
    def __repr__(self):
        return "<OpenCL Context: %d>" % self.id

class OpenCLQueuesManager(base.Manager):
    
    resource_class = OpenCLQueue

    def list(self):
        """List all opencl queues."""
        url = "/os-openclqueues"
        resp = self._list(url, "Queues", obj_class=OpenCLQueueId)
        listQueues = []
        for queue in resp:
            listQueues.append(queue.id)
        return listQueues

    def show(self, queue_id):
        """show the parameters of queue id"""
        url = "/os-openclqueues/%d" % queue_id
        return self._get(url, "Queue")

    def create(self, Device, Context, listProperties):
        """
        Create a new context using the devices in the list
        with properties listProperties
        """
        url = "/os-openclqueues"
        body = {'Device': Device, 'Context': Context}
        resp = self._create(url, body, 'CreateResp', return_raw=True)
        return (resp['id'], resp['CL_ERROR_CODE'])

    def retain(self, queue_id):
        """
        Retain a queue
        """
        url = "/os-openclqueues/%d/retain" % queue_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def release(self, queue_id):
        """
        Release a queue
        """
        url = "/os-openclqueues/%d/release" % queue_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
        
    def enqueuereadbuffer(self, queue_id, buffer_id, ByteCount, blocking_read=True, Offset=0,
                          wait_event_list=None, done_event=None):
        """
        enqueue a read buffer operation
        """
        url = "/os-openclqueues/%d/enqueuereadbuffer" % queue_id
        body = {'Buffer': buffer_id,
                'Offset': Offset, 'ByteCount': ByteCount}
        resp = self._create(url, body, "ReadBufferResp", return_raw=True)
        binaryData = bytearray(binascii.a2b_base64( str(resp['Data']) ))
        return (binaryData, resp['CL_ERROR_CODE'])
 
    def enqueuewritebuffer(self, queue_id, buffer_id, ByteCount, data, blocking_write=True, Offset=0,
                          wait_event_list=None, done_event=None):
        """
        enqueue a write buffer operation
        """
        url = "/os-openclqueues/%d/enqueuewritebuffer" % queue_id
        # we assume that data is bytearray; we have to convert to base64
        base64data = ""
        StartPosition = 0
        while StartPosition < ByteCount:
            EndPosition = StartPosition + 57
            if EndPosition > ByteCount:
                EndPosition = ByteCount
            Data2Convert = bytearray(data[StartPosition : EndPosition])
            StartPosition = EndPosition
            base64Slice = binascii.b2a_base64(Data2Convert)
            base64data = base64data + base64Slice
        body = {'Buffer': buffer_id,
                'Offset': Offset, 'ByteCount': ByteCount,
                'Data': base64data}
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
 
    def enqueuecopybuffer(self, queue_id, source_buffer_id, destination_buffer_id, 
                          ByteCount,
                          blocking_copy=True, 
                          source_offset=0, destination_offset=0, 
                          wait_event_list=None, done_event=None):
        """
        enqueues a copy buffer operation
        """
        url = "/os-openclqueues/%d/enqueuecopybuffer" % queue_id
        body = {'SourceBuffer': source_buffer_id, 
                'DestinationBuffer': destination_buffer_id,
                'SourceOffset': source_offset,
                'DestinationOffset': destination_offset, 
                'ByteCount': ByteCount}
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def enqueuendrangekernel(self, queue_id, kernel_id, 
                             global_size, global_offset, local_size,
                             wait_event_list=None, done_event=None):
        """
        enque an ND range kernel
        """
        url = "/os-openclqueues/%d/enqueuendrangekernel" % queue_id
        global_size_dict = []
        for sz in global_size:
            global_size_dict.append({'Size': sz})
        local_size_dict = []
        for sz in local_size:
            local_size_dict.append({'Size': sz})
        global_offset_dict = []
        for sz in global_offset:
            global_offset_dict.append({'Size': sz})
        body = {'Kernel': kernel_id, 
                'GlobalWorkSize': global_size_dict,
                'GlobalWorkOffset': global_offset_dict,
                'LocalWorkSize': local_size_dict}
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
 
    def enqueuetask(self, queue_id, kernel_id, 
                    wait_event_list=None, done_event=None):
        """
        enque a task
        """
        url = "/os-openclqueues/%d/enqueuetask" % queue_id
        body = {'Kernel': kernel_id}
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def enqueuebarrier(self, queue_id):
        """
        enqueue a barrier
        """
        url = "/os-openclqueues/%d/enqueuebarrier" % queue_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
 
    def finish(self, queue_id):
        """
        finish
        """
        url = "/os-openclqueues/%d/finish" % queue_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

