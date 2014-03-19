import unittest
import PyOpenCLInterface
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

    def setUp(self):
        retErr = PyOpenCLInterface.Initialize(self.testResources.device_type)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        pass

    def testCreateMemBuffer(self):
        """Creates a new context"""
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        # create mem buffer
        bufferSize = 512
        bufferCreateFlags = []
        bufferID, retErr = PyOpenCLInterface.CreateBuffer(contextID, bufferSize, bufferCreateFlags)
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [bufferID])
        bufferProperty, retErr = PyOpenCLInterface.GetBufferProperties(bufferID)
        self.assertEqual(bufferProperty['id'], bufferID)
        self.assertEqual(bufferProperty['Size'], bufferSize)
        self.assertEqual(bufferProperty['Context'], contextID)
        retErr = PyOpenCLInterface.ReleaseBuffer(bufferID)
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testGetUnknownContextProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        bufferID = 0
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.GetBufferProperties, bufferID)
       
    def testRetainAndRelease(self):
        """
        Create and release a context
        """
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        bufferSize = 512
        bufferAttribs = []
        bufferID, retErr = PyOpenCLInterface.CreateBuffer(contextID, bufferSize, bufferAttribs)
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [bufferID])
        retErr = PyOpenCLInterface.ReleaseBuffer( bufferID )
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [])
        # try to release again
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.RetainBuffer, bufferID)
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testMultipleBuffers(self):
        """
        Creates multiple buffers
        """
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        buffer1Size = 512
        bufferAttribs = []
        buffer1ID, retErr = PyOpenCLInterface.CreateBuffer(contextID, buffer1Size, bufferAttribs)
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [buffer1ID])
        buffer2Size = 1024
        bufferAttribs = []
        buffer2ID, retErr = PyOpenCLInterface.CreateBuffer(contextID, buffer2Size, bufferAttribs)
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [buffer1ID, buffer2ID])
        buffer1Property, retErr = PyOpenCLInterface.GetBufferProperties(buffer1ID)
        self.assertEqual(buffer1Property['id'], buffer1ID)
        self.assertEqual(buffer1Property['Size'], buffer1Size)
        self.assertEqual(buffer1Property['Context'], contextID)
        buffer2Property, retErr = PyOpenCLInterface.GetBufferProperties(buffer2ID)
        self.assertEqual(buffer2Property['id'], buffer2ID)
        self.assertEqual(buffer2Property['Size'], buffer2Size)
        self.assertEqual(buffer2Property['Context'], contextID)
        retErr = PyOpenCLInterface.ReleaseBuffer( buffer1ID )
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [buffer2ID])
        retErr = PyOpenCLInterface.ReleaseBuffer( buffer2ID )
        self.assertEqual(retErr, 0)
        listBuffers = PyOpenCLInterface.ListBuffers()
        self.assertEqual(listBuffers, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

if __name__ == "__main__":
    unittest.main()

