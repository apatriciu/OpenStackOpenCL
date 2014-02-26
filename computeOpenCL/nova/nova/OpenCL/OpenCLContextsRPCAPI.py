import OpenCLRPCAPI

class OpenCLContextsRPCAPI(OpenCLRPCAPI.OpenCLRPCAPI):
    def __init__(self):
        super(OpenCLContextsRPCAPI, self).__init__(routing_key = 'opencl.contexts', 
                                                   exchange = 'opencl',
                                                   respQueueName = "ContextsResponseChannel")

    def ListContexts(self):
        return self.CallServer('ListContexts')

    def GetContextProperties(self, id):
        return self.CallServer('GetContextProperties', {'id': id})

    def CreateContext(self, listDevicesIDs, dictProperties):
        return self.CallServer('CreateContext', {'Devices': listDevicesIDs, 'Properties': dictProperties})

    def ReleaseContext(self, id):
        return self.CallServer('ReleaseContext', {'id': id})

    def RetainContext(self, id):
        return self.CallServer('RetainContext', {'id': id})

