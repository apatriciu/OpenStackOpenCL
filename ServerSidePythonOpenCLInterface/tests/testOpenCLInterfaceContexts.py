import unittest
import PyOpenCLInterface
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    contextID = 0
    invalidContext = 1
    device_type = "GPU"

class TestContexts(unittest.TestCase):
    # define the expected response

    def setUp(self):
        self.testResources = LaptopResources()
        retErr = PyOpenCLInterface.Initialize(self.testResources.device_type)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        pass

    def testCreateContext(self):
        """Creates a new context"""
        try:
            listContexts = PyOpenCLInterface.ListContexts()
            self.assertEqual(listContexts, [])
            contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
            self.assertEqual(contextID, self.testResources.contextID)
            self.assertEqual(retErr, 0)
            listContexts = PyOpenCLInterface.ListContexts()
            self.assertEqual(listContexts, [contextID])
            retErr = PyOpenCLInterface.ReleaseContext(contextID)
            self.assertEqual(retErr, 0)
            listContexts = PyOpenCLInterface.ListContexts()
            self.assertEqual(listContexts, [])
        except:
            print "Exception caught:", sys.exc_info()[0]

    def testGetContextProperties(self):
        """Retrieves the properties of a context"""
        try:
            contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
            contextProps, retErr = PyOpenCLInterface.GetContextProperties(contextID)
            self.assertEqual(retErr, 0)
            self.assertEqual(contextProps['id'], contextID)
            self.assertEqual(contextProps['Devices'], self.testResources.listDevicesIDs)
            retErr = PyOpenCLInterface.ReleaseContext(contextID)
        except:
            print "Exception caught:", sys.exc_info()[0]

    def testGetUnknownContextProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        try:
            """ make sure that there are no contexts """
            listContexts = PyOpenCLInterface.ListContexts()
            self.assertEqual(listContexts, [])
        except:
            print "Exception caught:", sys.exc_info()[0]
            self.assertEqual(1, 0)
        contextID = 0
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.GetContextProperties, contextID)
        
    def testRetainAndRelease(self):
        """
        Create and release a context
        """
        try:
            contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
            contextProps, retErr = PyOpenCLInterface.GetContextProperties(contextID)
            self.assertEqual(retErr, 0)
            self.assertEqual(contextProps['id'], contextID)
            self.assertEqual(contextProps['Devices'], self.testResources.listDevicesIDs)
            retErr = PyOpenCLInterface.ReleaseContext(contextID)
        except:
            print "Exception caught:", sys.exc_info()[0]
            self.assertEqual(1, 0)
        # try to release again
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.RetainContext, contextID)

if __name__ == "__main__":
    unittest.main()

