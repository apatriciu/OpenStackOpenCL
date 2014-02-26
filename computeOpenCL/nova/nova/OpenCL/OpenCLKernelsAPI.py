import OpenCLKernelsRPCAPI
import sys

class API(object):
    def __init__(self):
        self.rpc_api = OpenCLKernelsRPCAPI.OpenCLKernelsRPCAPI()

    def ListKernels(self):
        resp = self.rpc_api.ListKernels()
        return resp[0]

    def GetKernelProperties(self, id):
        resp = self.rpc_api.GetKernelProperties(id)
        return (resp[0], resp[1])

    def CreateKernel(self, program, kernelName):
        resp = self.rpc_api.CreateKernel(program, kernelName)
        return (resp[0], resp[1])

    def RetainKernel(self, id):
        resp = self.rpc_api.RetainKernel(id)
        return resp

    def ReleaseKernel(self, id):
        resp = self.rpc_api.ReleaseKernel(id)
        return resp

    def KernelSetArgument(self, id, paramIndex, paramDict):
        resp = self.rpc_api.KernelSetArgument(id, paramIndex, paramDict)
        return resp


