import OpenCLDevicesRPCAPI
import sys

class API(object):
    def __init__(self):
        self.rpc_api = OpenCLDevicesRPCAPI.OpenCLDevicesRPCAPI()

    def ListDevices(self):
        resp = self.rpc_api.ListDevices()
        return (resp[0], resp[1]) 

    def GetDeviceProperties(self, id):
        resp = self.rpc_api.GetDeviceProperties(id)
        return (resp[0], resp[1])
    
if __name__ == "__main__":
    devAPI = API()
    try:
        print devAPI.ListDevices()
        print devAPI.GetDeviceProperties(0)
    except:
        print "Exception caught : %s " % sys.exc_info()[0]

