import unittest
import PyOpenCLInterface
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    invalidQueueID = 1
    device_type = "GPU"

class TestQueues(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()

    def setUp(self):
        retErr = PyOpenCLInterface.Initialize(self.testResources.device_type)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        pass

    def testCreateQueue(self):
        """Creates a new context"""
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        # create mem queue
        queueCreateFlags = []
        queueID, retErr = PyOpenCLInterface.CreateQueue(contextID, self.testResources.listDevicesIDs[0], queueCreateFlags)
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [queueID])
        queueProperty, retErr = PyOpenCLInterface.GetQueueProperties(queueID)
        self.assertEqual(queueProperty['id'], queueID)
        self.assertEqual(queueProperty['Device'], self.testResources.listDevicesIDs[0])
        self.assertEqual(queueProperty['Context'], contextID)
        retErr = PyOpenCLInterface.ReleaseQueue(queueID)
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testGetUnknownObjectProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        queueID = 0
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.GetQueueProperties, queueID)
       
    def testRetainAndRelease(self):
        """
        Create and release a context
        """
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueAttribs = []
        queueID, retErr = PyOpenCLInterface.CreateQueue(contextID, self.testResources.listDevicesIDs[0], queueAttribs)
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [queueID])
        retErr = PyOpenCLInterface.ReleaseQueue( queueID )
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [])
        # try to release again
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.RetainQueue, queueID)
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testMultipleQueues(self):
        """
        Creates multiple queues
        """
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueAttribs = []
        queue1ID, retErr = PyOpenCLInterface.CreateQueue(contextID, self.testResources.listDevicesIDs[0], queueAttribs)
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [queue1ID])
        queueAttribs = []
        queue2ID, retErr = PyOpenCLInterface.CreateQueue(contextID, self.testResources.listDevicesIDs[0], queueAttribs)
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [queue1ID, queue2ID])
        queue1Property, retErr = PyOpenCLInterface.GetQueueProperties(queue1ID)
        self.assertEqual(queue1Property['id'], queue1ID)
        self.assertEqual(queue1Property['Device'], self.testResources.listDevicesIDs[0])
        self.assertEqual(queue1Property['Context'], contextID)
        queue2Property, retErr = PyOpenCLInterface.GetQueueProperties(queue2ID)
        self.assertEqual(queue2Property['id'], queue2ID)
        self.assertEqual(queue2Property['Device'], self.testResources.listDevicesIDs[0])
        self.assertEqual(queue2Property['Context'], contextID)
        retErr = PyOpenCLInterface.ReleaseQueue( queue1ID )
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [queue2ID])
        retErr = PyOpenCLInterface.ReleaseQueue( queue2ID )
        self.assertEqual(retErr, 0)
        listQueues = PyOpenCLInterface.ListQueues()
        self.assertEqual(listQueues, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

if __name__ == "__main__":
    unittest.main()

