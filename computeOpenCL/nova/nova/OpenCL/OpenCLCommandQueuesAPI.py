import OpenCLCommandQueuesRPCAPI
import sys

class API(object):
    def __init__(self):
        self.rpc_api = OpenCLCommandQueuesRPCAPI.OpenCLCommandQueuesRPCAPI()

    def ListQueues(self):
        resp = self.rpc_api.ListCommandQueues()
        return resp[0]

    def GetQueueProperties(self, id):
        resp = self.rpc_api.GetCommandQueueProperties(id)
        return (resp[0], resp[1])

    def CreateQueue(self, context, device, flags):
        resp = self.rpc_api.CreateCommandQueue(context, device, flags)
        return (resp[0], resp[1])

    def RetainQueue(self, id):
        resp = self.rpc_api.RetainCommandQueue(id)
        return resp

    def ReleaseQueue(self, id):
        resp = self.rpc_api.ReleaseCommandQueue(id)
        return resp

    def EnqueueReadBuffer(self, id, membuffer, bytecount, offset, containerid, swiftcontext):
        resp = self.rpc_api.EnqueueReadBuffer(id, membuffer, bytecount, offset, containerid, swiftcontext)
        return resp

    def EnqueueWriteBuffer(self, id, membuffer, bytecount, offset, dataobject, containerid, swiftcontext):
        resp = self.rpc_api.EnqueueWriteBuffer(id, membuffer, bytecount, offset, dataobject, containerid, swiftcontext)
        return resp

    def EnqueueCopyBuffer(self, id, sourcebuffer, destinationbuffer,
                                  sourceoffset, destinationoffset, bytecount):
        resp = self.rpc_api.EnqueueCopyBuffer(id,  sourcebuffer, destinationbuffer,
                                  sourceoffset, destinationoffset, bytecount)
        return resp

    def EnqueueNDRangeKernel(self, id, kernel, gwo, gws, lws):
        resp = self.rpc_api.EnqueueNDRangeKernel(id, kernel, gwo, gws, lws)
        return resp

    def EnqueueTask(self, id, kernel):
        resp = self.rpc_api.EnqueueTask(id, kernel)
        return resp

    def EnqueueBarrier(self, id):
        resp = self.rpc_api.EnqueueBarrier(id)
        return resp

    def Finish(self, id):
        resp = self.rpc_api.Finish(id)
        return resp

