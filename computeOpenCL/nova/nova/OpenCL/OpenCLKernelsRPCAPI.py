import OpenCLRPCAPI

class OpenCLKernelsRPCAPI(OpenCLRPCAPI.OpenCLRPCAPI):
    def __init__(self):
        super(OpenCLKernelsRPCAPI, self).__init__(routing_key = 'opencl.kernels', 
                                                   exchange = 'opencl',
                                                   respQueueName = "KernelsResponseChannel")

    def ListKernels(self):
        return self.CallServer('ListKernels')

    def GetKernelProperties(self, id):
        return self.CallServer('GetKernelProperties', {'id': id})

    def CreateKernel(self, program, kernel_name):
        return self.CallServer('CreateKernel', {'Program': program, 
                                                'KernelName': kernel_name})

    def ReleaseKernel(self, id):
        return self.CallServer('ReleaseKernel', {'id': id})

    def RetainKernel(self, id):
        return self.CallServer('RetainKernel', {'id': id})

    def KernelSetArgument(self, id, paramIndex, paramDict):
        return self.CallServer('KernelSetArgument', {'id': id, 
                                                'ParamIndex': paramIndex,
                                                'ParamDict': paramDict})


