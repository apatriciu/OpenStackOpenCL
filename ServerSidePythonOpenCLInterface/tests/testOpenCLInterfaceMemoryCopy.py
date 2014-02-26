import unittest
import PyOpenCLInterface
import PyTestObjects
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    device_type = "GPU"

class TestQueuesMemCopy(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()

    def setUp(self):
        retErr = PyOpenCLInterface.Initialize(self.testResources.device_type)
        self.assertEqual(retErr, 0)
        self.contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueCreateFlags = []
        self.queueID, retErr = PyOpenCLInterface.CreateQueue(self.contextID, self.testResources.listDevicesIDs[0], queueCreateFlags)
        self.assertEqual(retErr, 0)
        self.longIntVal = 101
        self.testByteArray = PyTestObjects.LongAsByteArray(self.longIntVal)
        self.bufferSize = len(self.testByteArray)
        bufferCreateFlags = []
        self.bufferID, retErr = PyOpenCLInterface.CreateBuffer(self.contextID, self.bufferSize, bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.bufferID2, retErr = PyOpenCLInterface.CreateBuffer(self.contextID, self.bufferSize, bufferCreateFlags)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = PyOpenCLInterface.ReleaseBuffer(self.bufferID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseBuffer(self.bufferID2)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseQueue(self.queueID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)


    def testWriteAndRead(self):
        """Creates a new context"""
        try:
            # copy to the device memory
            retErr = PyOpenCLInterface.EnqueueWriteBuffer(self.queueID, self.bufferID, self.bufferSize, 0, self.testByteArray)
            self.assertEqual(retErr, 0)
            retData, retErr = PyOpenCLInterface.EnqueueReadBuffer(self.queueID, self.bufferID, self.bufferSize, 0)
            self.assertEqual(len(retData), self.bufferSize)
            self.assertEqual(retErr, 0)
            retValue = PyTestObjects.ByteArrayAsLong( retData )
            self.assertEqual(retValue, self.longIntVal)
        except:
            print "Exception caught:", sys.exc_info()[0]

    def testWriteCopyRead(self):
        """Creates a new context"""
        try:
            # copy to the device memory
            retErr = PyOpenCLInterface.EnqueueWriteBuffer(self.queueID, self.bufferID, self.bufferSize, 0, self.testByteArray)
            self.assertEqual(retErr, 0)
            retErr = PyOpenCLInterface.EnqueueCopyBuffer(self.queueID, self.bufferID, self.bufferID2, self.bufferSize, 0, 0)
            self.assertEqual(retErr, 0)
            retErr = PyOpenCLInterface.EnqueueBarrier(self.queueID)
            self.assertEqual(retErr, 0)
            retData, retErr = PyOpenCLInterface.EnqueueReadBuffer(self.queueID, self.bufferID2, self.bufferSize, 0)
            self.assertEqual(len(retData), self.bufferSize)
            self.assertEqual(retErr, 0)
            retValue = PyTestObjects.ByteArrayAsLong( retData )
            self.assertEqual(retValue, self.longIntVal)
        except:
            print "Exception caught:", sys.exc_info()[0]

if __name__ == "__main__":
    unittest.main()

