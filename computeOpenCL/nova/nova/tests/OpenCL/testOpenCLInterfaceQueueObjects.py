import unittest
from nova.OpenCL import OpenCLContextsAPI
from nova.OpenCL import OpenCLClientException
from nova.OpenCL import OpenCLCommandQueuesAPI
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    invalidQueueID = 1
    device_type = "GPU"

class TestQueues(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    contexts_interface = OpenCLContextsAPI.API()
    command_queues_interface = OpenCLCommandQueuesAPI.API()

    def setUp(self):
        self.contextID, retErr = self.contexts_interface.CreateContext(self.testResources.listDevicesIDs, 
                                                                       self.testResources.dictProperties)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = self.contexts_interface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)

    def testCreateQueue(self):
        # create mem queue
        queueCreateFlags = []
        queueID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                                               self.testResources.listDevicesIDs[0], 
                                               queueCreateFlags)
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [queueID])
        queueProperty, retErr = self.command_queues_interface.GetQueueProperties(queueID)
        self.assertEqual(queueProperty['id'], queueID)
        self.assertEqual(queueProperty['Device'], self.testResources.listDevicesIDs[0])
        self.assertEqual(queueProperty['Context'], self.contextID)
        retErr = self.command_queues_interface.ReleaseQueue(queueID)
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [])

    def testGetUnknownObjectProperties(self):
        queueID = 0
        self.assertRaises(OpenCLClientException.OpenCLClientException, 
                      self.command_queues_interface.GetQueueProperties, 
                      queueID)
       
    def testRetainAndRelease(self):
        queueAttribs = []
        queueID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                                               self.testResources.listDevicesIDs[0], 
                                               queueAttribs)
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [queueID])
        retErr = self.command_queues_interface.ReleaseQueue( queueID )
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [])
        # try to release again
        self.assertRaises(OpenCLClientException.OpenCLClientException, 
                      self.command_queues_interface.ReleaseQueue, 
                      queueID)
        self.assertRaises(OpenCLClientException.OpenCLClientException, 
                      self.command_queues_interface.RetainQueue, 
                      queueID)

    def testMultipleQueues(self):
        queueAttribs = []
        queue1ID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                                                self.testResources.listDevicesIDs[0], 
                                                queueAttribs)
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [queue1ID])
        queueAttribs = []
        queue2ID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                                                self.testResources.listDevicesIDs[0], 
                                                queueAttribs)
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [queue1ID, queue2ID])
        queue1Property, retErr = self.command_queues_interface.GetQueueProperties(queue1ID)
        self.assertEqual(queue1Property['id'], queue1ID)
        self.assertEqual(queue1Property['Device'], self.testResources.listDevicesIDs[0])
        self.assertEqual(queue1Property['Context'], self.contextID)
        queue2Property, retErr = self.command_queues_interface.GetQueueProperties(queue2ID)
        self.assertEqual(queue2Property['id'], queue2ID)
        self.assertEqual(queue2Property['Device'], self.testResources.listDevicesIDs[0])
        self.assertEqual(queue2Property['Context'], self.contextID)
        retErr = self.command_queues_interface.ReleaseQueue( queue1ID )
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [queue2ID])
        retErr = self.command_queues_interface.ReleaseQueue( queue2ID )
        self.assertEqual(retErr, 0)
        listQueues = self.command_queues_interface.ListQueues()
        self.assertEqual(listQueues, [])

if __name__ == "__main__":
    unittest.main()

