from Dispatch import Dispatch
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager

class OpenCLCommandQueuesManager(Dispatch, OpenCLResourcesAliasManager):

    def __init__(self, rpcclient, openclnodes, openclcontexts,
                       opencldevices, openclbuffers, openclprograms,
                       openclkernels):
        self.nodemanager = openclnodes
        self.contextsmanager = openclcontexts
        self.devicesmanager = opencldevices
        self.buffersmanager = openclbuffers
        self.programsmanager = openclprograms
        self.kernelsmanager = openclkernels
        self.rpcclient = rpcclient
        Dispatch.__init__(self)
        OpenCLResourcesAliasManager.__init__(self)

    def ListCommandQueues(self, args = None):
        try:
            lc = self.List()
            retErr = 0
        except:
            lc = []
            retErr = 0
        return (lc, retErr)

    def GetCommandQueueProperties(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            newargs = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'GetCommandQueueProperties',
                                       args = newargs)
            ocldev = result[0]['Device']
            oclctxt = result[0]['Context']
            nErr = result[1]
            CommandQueueProperties = result[0]
            CommandQueueProperties['id'] = nid
            devID = self.devicesmanager.FromNodeAndID(nodeID, ocldev)
            ctxtID = self.contextsmanager.FromNodeAndID(nodeID, oclctxt)
            CommandQueueProperties['Device'] = devID
            CommandQueueProperties['Context'] = ctxtID
        except:
            nErr = -128
            CommandQueueProperties = {}
        return (CommandQueueProperties, nErr)

    def CreateCommandQueue(self, args):
        try:
            context = int(args['Context'])
            ncID, contextID = self.contextsmanager.FromAlias(context)
            device = int(args['Device'])
            nodeID, deviceID = self.devicesmanager.FromAlias(device)
            if (ncID != nodeID):
                raise Exception('Context and Device should be on the same node')
            createFlags = args['Properties']
            newargs = {'Context': contextID, 'Device': deviceID, 'Properties': createFlags}
            respCreateCQ = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'CreateCommandQueue',
                                       args = newargs)
            aliasID = self.Insert(nodeID, respCreateCQ[0])
        except:
            return -128
        return aliasID, respCreateCQ[1]

    def ReleaseCommandQueue(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'ReleaseCommandQueue',
                                       args = args)
            if result <= 0:
                self.Delete(nid)
        except:
            return -128
        return result

    def RetainCommandQueue(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'RetainCommandQueue',
                                       args = args)
        except:
            return -128
        return result

    def EnqueueReadBuffer(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            membuffer = int(args['MemBuffer'])
            nodebufferID, bufferID = self.buffersmanager.FromAlias(membuffer)
            if (nodeID != nodebufferID):
                raise Exception("Queue and Memory Object have to reside on the same node")
            bytecount = int(args['ByteCount'])
            offset = int(args['Offset'])
            swift_container = args['ContainerId']
            swift_context = args['SwiftContext']
            newargs = {'id': ID, 
                       'MemBuffer': bufferID,
                       'ByteCount': bytecount,
                       'Offset': offset,
                       'ContainerId': swift_container,
                       'SwiftContext': swift_context}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'EnqueueReadBuffer',
                                       args = newargs)
        except:
            return -128
        return result

    def EnqueueWriteBuffer(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            membuffer = int(args['MemBuffer'])
            nodebufferID, bufferID = self.buffersmanager.FromAlias(membuffer)
            if (nodeID != nodebufferID):
                raise Exception("Queue and Memory Object have to reside on the same node")
            bytecount = int(args['ByteCount'])
            offset = int(args['Offset'])
            swift_container = args['ContainerId']
            swift_object = args['DataObjectId']
            swift_context = args['SwiftContext']
            newargs = {'id': ID, 
                       'MemBuffer': bufferID,
                       'ByteCount': bytecount,
                       'Offset': offset,
                       'ContainerId': swift_container,
                       'DataObjectId': swift_object,
                       'SwiftContext': swift_context}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'EnqueueWriteBuffer',
                                       args = newargs)
        except:
            return -128
        return result

    def EnqueueCopyBuffer(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            sourcebuffer = int(args['SourceBuffer'])
            nodesbufferID, sbufferID = self.buffersmanager.FromAlias(sourcebuffer)
            if (nodeID != nodesbufferID):
                raise Exception("Queue and Memory Object have to reside on the same node")
            destinationbuffer = int(args['DestinationBuffer'])
            nodedbufferID, dbufferID = self.buffersmanager.FromAlias(destinationbuffer)
            if (nodeID != nodedbufferID):
                raise Exception("Queue and Memory Object have to reside on the same node")
            bytecount = int(args['ByteCount'])
            sourceoffset = int(args['SourceOffset'])
            destinationoffset = int(args['DestinationOffset'])
            newargs = {'id': ID, 
                       'SourceBuffer': sbufferID,
                       'DestinationBuffer': dbufferID,
                       'ByteCount': bytecount,
                       'SourceOffset': sourceoffset,
                       'DestinationOffset': destinationoffset}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'EnqueueCopyBuffer',
                                       args = newargs)
        except:
            return -128
        return result

    def EnqueueNDRangeKernel(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            kernel = int(args['Kernel'])
            nodekernelID, kernelID = self.kernelsmanager.FromAlias(kernel)
            if (nodeID != nodekernelID):
                raise Exception("Queue and Memory Object have to reside on the same node")
            gwo = args['GWO']
            gws = args['GWS']
            lws = args['LWS']
            newargs = {'id': ID,
                       'Kernel': kernelID,
                       'GWO': gwo, 'GWS': gws, 'LWS': lws}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'EnqueueNDRangeKernel',
                                       args = newargs)
        except:
            return -128
        return result

    def EnqueueTask(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            kernel = int(args['Kernel'])
            nodekernelID, kernelID = self.kernelsmanager.FromAlias(kernel)
            if (nodeID != nodekernelID):
                raise Exception("Queue and Memory Object have to reside on the same node")
            newargs = {'id': ID,
                       'Kernel': kernelID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'EnqueueTask',
                                       args = newargs)
        except:
            return -128
        return result

    def EnqueueBarrier(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'EnqueueBarrier',
                                       args = args)
        except:
            return -128
        return result

    def Finish(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".commandqueues",
                                       method = 'Finish',
                                       args = args)
        except:
            return -128
        return result


