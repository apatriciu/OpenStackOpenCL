import unittest
from nova.OpenCL import OpenCLContextsAPI
from nova.OpenCL import OpenCLClientException
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    invalidContext = 5
    device_type = "GPU"

class TestContexts(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    contextsAPI = OpenCLContextsAPI.API()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreateContext(self):
        """Creates a new context"""
        listContexts = self.contextsAPI.ListContexts()
        self.assertEqual(listContexts, [])
        contextID, retErr = self.contextsAPI.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        listContexts = self.contextsAPI.ListContexts()
        self.assertEqual(listContexts, [contextID])
        retErr = self.contextsAPI.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)
        listContexts = self.contextsAPI.ListContexts()
        self.assertEqual(listContexts, [])

    def testGetContextProperties(self):
        """Retrieves the properties of a context"""
        contextID, retErr = self.contextsAPI.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        contextProps, retErr = self.contextsAPI.GetContextProperties(contextID)
        self.assertEqual(retErr, 0)
        self.assertEqual(contextProps['id'], contextID)
        self.assertEqual(contextProps['Devices'], self.testResources.listDevicesIDs)
        retErr = self.contextsAPI.ReleaseContext(contextID)

    def testGetUnknownContextProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        """ make sure that there are no contexts """
        listContexts = self.contextsAPI.ListContexts()
        self.assertEqual(listContexts, [])
        contextID = 0
        self.assertRaises(OpenCLClientException.OpenCLClientException, 
                          self.contextsAPI.GetContextProperties, 
                          contextID)
        
    def testRetainAndRelease(self):
        """
        Create and release a context
        """
        contextID, retErr = self.contextsAPI.CreateContext(self.testResources.listDevicesIDs, 
                                                           self.testResources.dictProperties)
        contextProps, retErr = self.contextsAPI.GetContextProperties(contextID)
        self.assertEqual(retErr, 0)
        self.assertEqual(contextProps['id'], contextID)
        self.assertEqual(contextProps['Devices'], self.testResources.listDevicesIDs)
        retErr = self.contextsAPI.ReleaseContext(contextID)
        # try to release again
        self.assertRaises(OpenCLClientException.OpenCLClientException, 
                          self.contextsAPI.ReleaseContext, 
                          contextID)
        self.assertRaises(OpenCLClientException.OpenCLClientException, 
                          self.contextsAPI.RetainContext, 
                          contextID)

if __name__ == "__main__":
    unittest.main()

