import OpenCLRPCAPI

class OpenCLDevicesRPCAPI(OpenCLRPCAPI.OpenCLRPCAPI):
    def __init__(self):
        super(OpenCLDevicesRPCAPI, self).__init__(routing_key = 'opencl.devices', 
                                                  exchange = 'opencl',
                                                  respQueueName = "DevicesResponseChannel")

    def ListDevices(self):
        return self.CallServer('ListDevices')

    def GetDeviceProperties(self, id):
        return self.CallServer('GetDeviceProperties', {'id': id})

