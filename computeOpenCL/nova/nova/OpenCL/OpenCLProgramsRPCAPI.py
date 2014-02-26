import OpenCLRPCAPI

class OpenCLProgramsRPCAPI(OpenCLRPCAPI.OpenCLRPCAPI):
    def __init__(self):
        super(OpenCLProgramsRPCAPI, self).__init__(routing_key = 'opencl.programs', 
                                                   exchange = 'opencl',
                                                   respQueueName = "ProgramsResponseChannel")

    def ListPrograms(self):
        return self.CallServer('ListPrograms')

    def GetProgramProperties(self, id):
        return self.CallServer('GetProgramProperties', {'id': id})

    def CreateProgram(self, context, programStrings):
        return self.CallServer('CreateProgram', {'Context': context, 
                                                'ProgramStrings': programStrings})

    def ReleaseProgram(self, id):
        return self.CallServer('ReleaseProgram', {'id': id})

    def RetainProgram(self, id):
        return self.CallServer('RetainProgram', {'id': id})

    def BuildProgram(self, id, listDevices, buildOptions):
        return self.CallServer('BuildProgram', {'id': id, 
                                                'Devices': listDevices,
                                                'Options': buildOptions})

    def GetProgramBuildInfo(self, id, device, buildInfo):
        return self.CallServer('GetProgramBuildInfo', {'id': id,
                                                       'Device': device,
                                                       'BuildInfo': buildInfo})

