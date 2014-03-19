from nova.api.openstack.compute.contrib import openclbuffersinterface as os_openclbuffersinterface
from nova.api.openstack.compute.contrib import openclinterface as os_openclinterface
import unittest
import webob
#from nova import test

class LaptopResponses:
    listDevicesOnSystem = [0]
    listDevicesIDs = [{"Device": 0}]
    testDevice = 0
    inexistentDevice = 1
    inexistentBuffer = 100
    dictProperties = {}
    contextID = 0
    invalidContext = 1
    device_type = "GPU"

class Request:
    environ = {'nova.context': {'user': 'guest', 'project': 'guest'}}

class OpenclbuffersinterfaceTestCase(unittest.TestCase):

    def setUp(self):
        # super(OpenclinterfaceTestCase, self).setUp();
        super(OpenclbuffersinterfaceTestCase, self).setUp()
        self.deviceResponses = LaptopResponses()
        self.Devices = os_openclinterface.OpenCLDevices()
        self.Contexts = os_openclinterface.OpenCLContexts()
        self.Buffers = os_openclbuffersinterface.OpenCLBuffers()
        req = Request()
        body = {'Devices': self.deviceResponses.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        self.contextID = resp['id']

    def tearDown(self):
        body = None
        req = Request()
        retErr = self.Contexts.release(req, str(self.contextID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

    def testCreateMemBuffer(self):
        """Creates a new context"""
            # create mem buffer
        req = Request()
        bufferSize = 512
        body = {'Context': self.contextID, 'MEM_SIZE': bufferSize, 'BufferProperties': []}
        bufferCreateResp = self.Buffers.create(req, body)['CreateResp']
        bufferID = bufferCreateResp['id']
        self.assertEqual(bufferCreateResp['CL_ERROR_CODE'], 0)
        listBuffers = self.Buffers.index(req)['Buffers']
        self.assertEqual(listBuffers, [{'id': bufferID}])
        body = None
        bufferProperties = self.Buffers.show(req, str(bufferID))['Buffer']
        self.assertEqual(bufferProperties['id'], bufferID)
        self.assertEqual(bufferProperties['MEM_SIZE'], bufferSize)
        self.assertEqual(bufferProperties['Context'], self.contextID)
        retErr = self.Buffers.release(req, str(bufferID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        listBuffers = self.Buffers.index(req)['Buffers']
        self.assertEqual(len(listBuffers), 0)

    def testGetUnknownBufferProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        req = Request()
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.Buffers.show,
                          req,
                          str(self.deviceResponses.inexistentBuffer))

    def testRetainRelease(self):
        """ Test retain and release """
        req = Request()
        listBuffers = self.Buffers.index(req)['Buffers']
        self.assertEqual(len(listBuffers), 0)
        bufferSize = 512
        body = {'Context': self.contextID, 'MEM_SIZE': bufferSize, 'BufferProperties': []}
        bufferCreateResp = self.Buffers.create(req, body)['CreateResp']
        bufferID = bufferCreateResp['id']
        self.assertEqual(bufferCreateResp['CL_ERROR_CODE'], 0)
        listBuffers = self.Buffers.index(req)['Buffers']
        self.assertEqual(len(listBuffers), 1)
        body = None
        retErr = self.Buffers.retain(req, str(bufferID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Buffers.release(req, str(bufferID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 1)
        retErr = self.Buffers.release(req, str(bufferID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        listBuffers = self.Buffers.index(req)['Buffers']
        self.assertEqual(len(listBuffers), 0)
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.Buffers.retain,
                          req,
                          str(bufferID),
                          body)
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.Buffers.release,
                          req,
                          str(bufferID),
                          body)

if __name__ == "__main__":
    unittest.main()

