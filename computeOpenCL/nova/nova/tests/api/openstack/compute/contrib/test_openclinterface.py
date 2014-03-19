from nova.api.openstack.compute.contrib import openclinterface as os_openclinterface
import unittest
import webob

#from nova import test

class LaptopGPUResponses:
    listDevicesOnSystem = [0]
    listDevicesIDs = [{"Device": 0}]
    deviceProperties = {'CL_DEVICE_MAX_MEM_ALLOC_SIZE': 134217728,
        'CL_DEVICE_MAX_COMPUTE_UNITS': 5,
        'CL_DEVICE_AVAILABLE': 1,
        'CL_DEVICE_LOCAL_MEM_SIZE': 32768,
        'CL_DEVICE_NAME': 'BeaverCreek',
        'CL_DEVICE_GLOBAL_MEM_SIZE': 268435456,
        'CL_DEVICE_MAX_WORK_GROUP_SIZE': 256,
        'id': 0,
        'CL_DEVICE_LOCAL_MEM_TYPE': 'CL_LOCAL',
        'CL_DEVICE_ENDIAN_LITTLE': 1}
    testDevice = 0
    inexistentDevice = 1
    inexistentContext = 100
    dictProperties = {}
    contextID = 0
    invalidContext = 1
    device_type = "GPU"

class LaptopCPUResponses:
    listDevicesOnSystem = [0]
    listDevicesIDs = [{"Device": 0}]
    deviceProperties = {'CL_DEVICE_MAX_MEM_ALLOC_SIZE': 2147483648,
                        'CL_DEVICE_MAX_COMPUTE_UNITS': 4,
                        'CL_DEVICE_AVAILABLE': 1,
                        'CL_DEVICE_ENDIAN_LITTLE': 1,
                        'CL_DEVICE_LOCAL_MEM_SIZE': 32768,
                        'CL_DEVICE_NAME': 'AMD A8-3500M APU with Radeon(tm) HD Graphics',
                        'CL_DEVICE_GLOBAL_MEM_SIZE': 5704847360,
                        'CL_DEVICE_MAX_WORK_GROUP_SIZE': 1024,
                        'id': 0,
                        'CL_DEVICE_LOCAL_MEM_TYPE': 'CL_GLOBAL'}
    testDevice = 0
    inexistentDevice = 2
    inexistentContext = 100
    dictProperties = {}
    contextID = 0
    invalidContext = 1
    device_type = "CPU"

class ServerGPUResponses:
    listDevicesOnSystem = [0, 1]
    listDevicesIDs = [{"Device": 0}]
    deviceProperties = {'CL_DEVICE_MAX_MEM_ALLOC_SIZE': 402440192,
                        'CL_DEVICE_MAX_COMPUTE_UNITS': 15,
                        'CL_DEVICE_AVAILABLE': 1,
                        'CL_DEVICE_ENDIAN_LITTLE': 1,
                        'CL_DEVICE_LOCAL_MEM_SIZE': 49152,
                        'CL_DEVICE_NAME': 'GeForce GTX 480',
                        'CL_DEVICE_GLOBAL_MEM_SIZE': 1609760768,
                        'CL_DEVICE_MAX_WORK_GROUP_SIZE': 1024,
                        'id': 0,
                        'CL_DEVICE_LOCAL_MEM_TYPE': 'CL_LOCAL'}
    testDevice = 0
    inexistentDevice = 2
    inexistentContext = 100
    dictProperties = {}
    contextID = 0
    invalidContext = 1
    device_type = "GPU"

class Request:
    environ = {'nova.context': {'user': 'guest', 'project': 'guest'}}

class OpenclinterfaceDevicesAndContextsTestCase(unittest.TestCase):

    def setUp(self):
        super(OpenclinterfaceDevicesAndContextsTestCase, self).setUp()
        self.deviceResponses = LaptopGPUResponses()
        self.Devices = os_openclinterface.OpenCLDevices()
        self.Contexts = os_openclinterface.OpenCLContexts();

    def test_devices_index(self):
        req = Request()
        ListDevs = self.Devices.index(req)['Devices']
        listDevices = []
        for dev in ListDevs:
            listDevices.append(dev['id'])
        self.assertEqual(listDevices, self.deviceResponses.listDevicesOnSystem)

    def test_devices_show(self):
        req = Request()
        resp = self.Devices.show(req, str(self.deviceResponses.testDevice))
        self.assertEqual(resp['Device']['CL_ERROR_CODE'], 0)
        deviceProps = resp['Device']
        for key, value in self.deviceResponses.deviceProperties.iteritems():
            # make sure that the returned key is in the 
            self.assertEqual( key in deviceProps, True )
            if key in deviceProps:
                self.assertEqual(value, deviceProps[key])

    def test_devices_show_unknown(self):
        req = Request()
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.Devices.show,
                          req,
                          str(self.deviceResponses.inexistentDevice))

    def testCreateContext(self):
        """Creates a new context"""
        req = Request()
        listContexts = self.Contexts.index(req)['Contexts']
        self.assertEqual(listContexts, [])
        body = {'Devices': self.deviceResponses.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        listContexts = self.Contexts.index(req)['Contexts']
        lstCtx = []
        for ctx in listContexts:
            lstCtx.append(ctx['id'])
        self.assertEqual(lstCtx, [resp['id']])
        id = str(resp['id'])
        retErr = self.Contexts.release(req, id, body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        listContexts = self.Contexts.index(req)['Contexts']
        self.assertEqual(listContexts, [])

    def testGetContextProperties(self):
        """Retrieves the properties of a context"""
        req = Request()
        body = {'Devices': self.deviceResponses.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        contextPropsResp = self.Contexts.show(req, str(resp['id']))['Context']
        self.assertEqual(contextPropsResp['CL_ERROR_CODE'], 0)
        contextProps = contextPropsResp
        self.assertEqual(contextProps['id'], resp['id'])
        self.assertEqual(contextProps['ListDevices'], self.deviceResponses.listDevicesIDs)
        body = None
        retErr = self.Contexts.release(req, str(resp['id']), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

    def testGetUnknownContextProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        req = Request()
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.Contexts.show,
                          req,
                          str(self.deviceResponses.inexistentContext))

    def testRetainAndRelease(self):
        """
        Create and release a context
        """
        req = Request()
        body = {'Devices': self.deviceResponses.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        body = None
        retErr = self.Contexts.retain(req, str(resp['id']), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Contexts.release(req, str(resp['id']), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 1)
        retErr = self.Contexts.release(req, str(resp['id']), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.Contexts.retain,
                          req,
                          str(resp['id']),
                          body)
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.Contexts.release,
                          req,
                          str(resp['id']),
                          body)

if __name__ == "__main__":
    unittest.main()

