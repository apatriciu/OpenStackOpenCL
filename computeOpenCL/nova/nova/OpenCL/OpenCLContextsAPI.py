import OpenCLContextsRPCAPI
import sys

class API(object):
    def __init__(self):
        self.rpc_api = OpenCLContextsRPCAPI.OpenCLContextsRPCAPI()

    def ListContexts(self):
        resp = self.rpc_api.ListContexts()
        return resp[0]

    def GetContextProperties(self, id):
        resp = self.rpc_api.GetContextProperties(id)
        return (resp[0], resp[1])

    def CreateContext(self, listDevicesIDs, dictProperties):
        resp = self.rpc_api.CreateContext(listDevicesIDs, dictProperties)
        return (resp[0], resp[1])

    def RetainContext(self, id):
        resp = self.rpc_api.RetainContext(id)
        return resp

    def ReleaseContext(self, id):
        resp = self.rpc_api.ReleaseContext(id)
        return resp

