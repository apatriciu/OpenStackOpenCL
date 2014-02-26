import OpenCLProgramsRPCAPI
import sys

class API(object):
    def __init__(self):
        self.rpc_api = OpenCLProgramsRPCAPI.OpenCLProgramsRPCAPI()

    def ListPrograms(self):
        resp = self.rpc_api.ListPrograms()
        return resp[0]

    def GetProgramProperties(self, id):
        resp = self.rpc_api.GetProgramProperties(id)
        return (resp[0], resp[1])

    def CreateProgram(self, context, programStrings):
        resp = self.rpc_api.CreateProgram(context, programStrings)
        return (resp[0], resp[1])

    def RetainProgram(self, id):
        resp = self.rpc_api.RetainProgram(id)
        return resp

    def ReleaseProgram(self, id):
        resp = self.rpc_api.ReleaseProgram(id)
        return resp

    def BuildProgram(self, id, listDevices, buildOptions):
        resp = self.rpc_api.BuildProgram(id, listDevices, buildOptions)
        return resp

    def GetProgramBuildInfo(self, id, device, buildInfo):
        resp = self.rpc_api.GetProgramBuildInfo(id, device, buildInfo)
        return resp

