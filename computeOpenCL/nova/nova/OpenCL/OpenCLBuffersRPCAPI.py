import OpenCLRPCAPI

class OpenCLBuffersRPCAPI(OpenCLRPCAPI.OpenCLRPCAPI):
    def __init__(self):
        super(OpenCLBuffersRPCAPI, self).__init__(routing_key = 'opencl.buffers', 
                                                   exchange = 'opencl',
                                                   respQueueName = "BuffersResponseChannel")

    def ListBuffers(self):
        return self.CallServer('ListBuffers')

    def GetBufferProperties(self, id):
        return self.CallServer('GetBufferProperties', {'id': id})

    def CreateBuffer(self, context, size, properties):
        return self.CallServer('CreateBuffer', {'Context': context, 
                                                'Size': size,
                                                'Properties': properties})

    def ReleaseBuffer(self, id):
        return self.CallServer('ReleaseBuffer', {'id': id})

    def RetainBuffer(self, id):
        return self.CallServer('RetainBuffer', {'id': id})

