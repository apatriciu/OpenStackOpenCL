import OpenCLBuffersRPCAPI
import sys

class API(object):
    def __init__(self):
        self.rpc_api = OpenCLBuffersRPCAPI.OpenCLBuffersRPCAPI()

    def ListBuffers(self):
        resp = self.rpc_api.ListBuffers()
        return resp[0]

    def GetBufferProperties(self, id):
        resp = self.rpc_api.GetBufferProperties(id)
        return (resp[0], resp[1])

    def CreateBuffer(self, context, size, properties):
        resp = self.rpc_api.CreateBuffer(context, size, properties)
        return (resp[0], resp[1])

    def RetainBuffer(self, id):
        resp = self.rpc_api.RetainBuffer(id)
        return resp

    def ReleaseBuffer(self, id):
        resp = self.rpc_api.ReleaseBuffer(id)
        return resp

