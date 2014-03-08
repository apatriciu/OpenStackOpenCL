import OpenCLRPCAPI

class OpenCLCommandQueuesRPCAPI(OpenCLRPCAPI.OpenCLRPCAPI):
    def __init__(self):
        super(OpenCLCommandQueuesRPCAPI, self).__init__(routing_key = 'opencl.commandqueues', 
                                                   exchange = 'opencl',
                                                   respQueueName = "CommandQueuesResponseChannel")

    def ListCommandQueues(self):
        return self.CallServer('ListCommandQueues')

    def GetCommandQueueProperties(self, id):
        return self.CallServer('GetCommandQueueProperties', {'id': id})

    def CreateCommandQueue(self, context, device, flags):
        return self.CallServer('CreateCommandQueue', {'Context': context, 
                                                'Device': device,
                                                'Properties': flags})

    def ReleaseCommandQueue(self, id):
        return self.CallServer('ReleaseCommandQueue', {'id': id})

    def RetainCommandQueue(self, id):
        return self.CallServer('RetainCommandQueue', {'id': id})

    def EnqueueReadBuffer(self, id, membuffer, bytecount, offset, containerid, swiftcontext):
        return self.CallServer('EnqueueReadBuffer', {'id': id, 'MemBuffer': membuffer,
                                                     'ByteCount': bytecount,
                                                     'Offset': offset,
                                                     'ContainerId': containerid,
                                                     'SwiftContext': swiftcontext})

    def EnqueueWriteBuffer(self, id, membuffer, bytecount, offset, dataobjectid, containerid, swiftcontext):
        return self.CallServer('EnqueueWriteBuffer', {'id': id, 'MemBuffer': membuffer,
                                                     'ByteCount': bytecount,
                                                     'Offset': offset,
                                                     'DataObjectId': dataobjectid,
                                                     'ContainerId': containerid,
                                                     'SwiftContext': swiftcontext})

    def EnqueueCopyBuffer(self, id, sourcebuffer, destinationbuffer,
                                  sourceoffset, destinationoffset, bytecount):
        return self.CallServer('EnqueueCopyBuffer', {'id': id, 
                                                     'SourceBuffer': sourcebuffer,
                                                     'DestinationBuffer': destinationbuffer,
                                                     'ByteCount': bytecount,
                                                     'SourceOffset': sourceoffset,
                                                     'DestinationOffset': destinationoffset})

    def EnqueueNDRangeKernel(self, id, kernel, gwo, gws, lws):
        return self.CallServer('EnqueueNDRangeKernel', {'id': id,
                                                        'Kernel': kernel,
                                                        'GWO': gwo,
                                                        'GWS': gws,
                                                        'LWS': lws})

    def EnqueueTask(self, id, kernel):
        return self.CallServer('EnqueueTask', {'id': id,
                                                 'Kernel': kernel})

    def EnqueueBarrier(self, id):
        return self.CallServer('EnqueueBarrier', {'id': id})

    def Finish(self, id):
        return self.CallServer('EnqueueFinish', {'id': id})

