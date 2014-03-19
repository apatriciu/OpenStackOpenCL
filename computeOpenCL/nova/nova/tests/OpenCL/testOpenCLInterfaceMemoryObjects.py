from nova.OpenCL import OpenCLContextsAPI
from nova.OpenCL import OpenCLClientException
from nova.OpenCL import OpenCLBuffersAPI
import unittest
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    memID = 0
    invalidMemID = 1
    device_type = "GPU"

class TestMems(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    contexts_interface = OpenCLContextsAPI.API()
    buffers_interface = OpenCLBuffersAPI.API()

    def setUp(self):
        """Creates a new context"""
        self.contextID, retErr = self.contexts_interface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = self.contexts_interface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)

    def testCreateMemBuffer(self):
        # create mem buffer
        bufferSize = 512
        bufferCreateFlags = []
        bufferID, retErr = self.buffers_interface.CreateBuffer(self.contextID, bufferSize, bufferCreateFlags)
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [bufferID])
        bufferProperty, retErr = self.buffers_interface.GetBufferProperties(bufferID)
        self.assertEqual(bufferProperty['id'], bufferID)
        self.assertEqual(bufferProperty['Size'], bufferSize)
        self.assertEqual(bufferProperty['Context'], self.contextID)
        retErr = self.buffers_interface.ReleaseBuffer(bufferID)
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [])

    def testGetUnknownContextProperties(self):
        # Tries to retrieve the properties of an inexistent device
        bufferID = 0
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.buffers_interface.GetBufferProperties, bufferID)
       
    def testRetainAndRelease(self):
        #  Create and release a context
        
        bufferSize = 512
        bufferAttribs = []
        bufferID, retErr = self.buffers_interface.CreateBuffer(self.contextID, bufferSize, bufferAttribs)
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [bufferID])
        retErr = self.buffers_interface.ReleaseBuffer( bufferID )
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [])
        # try to release again
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.buffers_interface.ReleaseBuffer, bufferID)
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.buffers_interface.RetainBuffer, bufferID)

    def testMultipleBuffers(self):
        # Creates multiple buffers
        buffer1Size = 512
        bufferAttribs = []
        buffer1ID, retErr = self.buffers_interface.CreateBuffer(self.contextID, buffer1Size, bufferAttribs)
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [buffer1ID])
        buffer2Size = 1024
        bufferAttribs = []
        buffer2ID, retErr = self.buffers_interface.CreateBuffer(self.contextID, buffer2Size, bufferAttribs)
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [buffer1ID, buffer2ID])
        buffer1Property, retErr = self.buffers_interface.GetBufferProperties(buffer1ID)
        self.assertEqual(buffer1Property['id'], buffer1ID)
        self.assertEqual(buffer1Property['Size'], buffer1Size)
        self.assertEqual(buffer1Property['Context'], self.contextID)
        buffer2Property, retErr = self.buffers_interface.GetBufferProperties(buffer2ID)
        self.assertEqual(buffer2Property['id'], buffer2ID)
        self.assertEqual(buffer2Property['Size'], buffer2Size)
        self.assertEqual(buffer2Property['Context'], self.contextID)
        retErr = self.buffers_interface.ReleaseBuffer( buffer1ID )
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [buffer2ID])
        retErr = self.buffers_interface.ReleaseBuffer( buffer2ID )
        self.assertEqual(retErr, 0)
        listBuffers = self.buffers_interface.ListBuffers()
        self.assertEqual(listBuffers, [])

if __name__ == "__main__":
    unittest.main()

