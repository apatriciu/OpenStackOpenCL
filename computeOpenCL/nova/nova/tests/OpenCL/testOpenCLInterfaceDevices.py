import unittest
from nova.OpenCL import OpenCLDevicesAPI
from nova.OpenCL import OpenCLClientException

class LaptopResponses:
    listDevicesOnSystem = [0]
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
    inexistentDevice = 2
    device_type = "GPU"

class LaptopCPUResponses:
    listDevicesOnSystem = [0]
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
    device_type = "CPU"

class ServerGPUResponses:
    listDevicesOnSystem = [0, 1]
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
    device_type = "GPU"

class TestDevices(unittest.TestCase):
    # define the expected response
    deviceResponses = LaptopResponses()
    devicesAPI = OpenCLDevicesAPI.API()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testListDevices(self):
        """Retrieves all the GPU devices available on the system"""
        listDevices, retErr = self.devicesAPI.ListDevices()
        self.assertEqual(listDevices, self.deviceResponses.listDevicesOnSystem)
        self.assertEqual(retErr, 0)

    def testGetDeviceProperties(self):
        """Retrieves the properties of a certain device """
        deviceProps, retErr = self.devicesAPI.GetDeviceProperties(self.deviceResponses.testDevice)
        for key, value in deviceProps.iteritems():
            # make sure that the returned key is in the 
            self.assertEqual( key in self.deviceResponses.deviceProperties, True )
            if key in self.deviceResponses.deviceProperties:
                self.assertEqual(value, self.deviceResponses.deviceProperties[key])
        self.assertEqual(retErr, 0)

    def testGetDevicePropertiesUnknownDevice(self):
        """Tries to retrieve the properties of an inexistent device"""
        self.assertRaises(OpenCLClientException.OpenCLClientException, 
                          self.devicesAPI.GetDeviceProperties, 
                          self.deviceResponses.inexistentDevice)

if __name__ == "__main__":
    unittest.main()

