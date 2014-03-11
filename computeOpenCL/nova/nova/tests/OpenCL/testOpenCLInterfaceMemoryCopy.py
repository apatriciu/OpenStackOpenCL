import unittest
from nova.OpenCL import OpenCLContextsAPI
from nova.OpenCL import OpenCLClientException
from nova.OpenCL import OpenCLCommandQueuesAPI
from nova.OpenCL import OpenCLBuffersAPI
import sys
import binascii
from binascii import unhexlify
from binascii import hexlify
import random
import SwiftTestUtils

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    device_type = "GPU"

class TestQueuesMemCopy(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    contexts_interface = OpenCLContextsAPI.API()
    buffers_interface = OpenCLBuffersAPI.API()
    command_queues_interface = OpenCLCommandQueuesAPI.API()
    stu = SwiftTestUtils.SwiftUtils()

    def setUp(self):
        self.contextID, retErr = self.contexts_interface.CreateContext(self.testResources.listDevicesIDs, 
                                                    self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueCreateFlags = []
        self.queueID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                                                    self.testResources.listDevicesIDs[0], 
                                                    queueCreateFlags)
        self.assertEqual(retErr, 0)
        self.RawString = bytearray("11111111")
        self.container = 'testcontainer'
        self.stu.createcontainer(self.container)
        self.objectname = 'testobject1'
        self.stu.createobject(objectname = self.objectname, 
                              objectdata = self.RawString,
                              container = self.container)
        self.bufferSize = len(self.RawString)
        bufferCreateFlags = []
        self.bufferID, retErr = self.buffers_interface.CreateBuffer(self.contextID, 
                                                    self.bufferSize, 
                                                    bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.bufferID2, retErr = self.buffers_interface.CreateBuffer(self.contextID, 
                                                    self.bufferSize, 
                                                    bufferCreateFlags)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferID)
        self.assertEqual(retErr, 0)
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferID2)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.ReleaseQueue(self.queueID)
        self.assertEqual(retErr, 0)
        retErr = self.contexts_interface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)
        self.stu.deleteobject(container = self.container, 
                              objectname = self.objectname)
        self.stu.deletecontainer(self.container)

    def testWriteAndRead(self):
        # copy to the device memory
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 
                                                    0, 
                                                    self.objectname,
                                                    self.container,
                                                    self.stu.getcontext() )
        self.assertEqual(retErr, 0)
        dataobjectid, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 0, 
                                                    self.container, 
                                                    self.stu.getcontext() )
        # retrieve from swift
        rawRetData = self.stu.getobjectdata( objectname = dataobjectid, container = self.container )
        self.assertEqual(len(rawRetData), self.bufferSize)
        self.assertEqual(retErr, 0)
        self.assertEqual(rawRetData, self.RawString)
        self.stu.deleteobject(container = self.container,
                              objectname = dataobjectid)

    def testWriteCopyRead(self):
        # copy to the device memory
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 
                                                    0, 
                                                    self.objectname,
                                                    self.container,
                                                    self.stu.getcontext())
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.EnqueueCopyBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferID2, 
                                                    0, 0,
                                                    self.bufferSize)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.EnqueueBarrier(self.queueID)
        self.assertEqual(retErr, 0)
        dataobjectid, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                                    self.bufferID2, self.bufferSize, 0, 
                                                    self.container, 
                                                    self.stu.getcontext() )
        # retrieve from swift
        rawRetData = self.stu.getobjectdata( objectname = dataobjectid, container = self.container )
        self.assertEqual(len(rawRetData), self.bufferSize)
        self.assertEqual(retErr, 0)
        self.assertEqual(rawRetData, self.RawString)
        self.stu.deleteobject(container = self.container,
                              objectname = dataobjectid)

if __name__ == "__main__":
    unittest.main()

