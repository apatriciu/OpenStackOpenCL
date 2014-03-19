from Dispatch import Dispatch
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager

class OpenCLKernelsManager(Dispatch, OpenCLResourcesAliasManager):

    def __init__(self, rpcclient, openclnodes, openclbuffers, 
                       openclprograms, openclcontexts):
        self.nodesmanager = openclnodes
        self.buffersmanager = openclbuffers
        self.programsmanager = openclprograms
        self.contextsmanager = openclcontexts
        self.rpcclient = rpcclient
        Dispatch.__init__(self)
        OpenCLResourcesAliasManager.__init__(self)

    def ListKernels(self, args = None):
        try:
            lk = self.map_resources.keys()
            retErr = 0
        except:
            lk = []
            retErr = -128
        return (lk, retErr)

    def GetKernelProperties(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            newargs = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".kernels",
                                       method = 'GetKernelProperties',
                                       args = newargs)
            nErr = result[1]
            KernelProperties = result[0]
            KernelProperties['id'] = nid
            prog = KernelProperties['Program']
            progID = self.programsmanager.FromNodeAndID(nodeID, prog)
            KernelProperties['Program'] = progID
            oclcontext = KernelProperties['Context']
            oclcontextID = self.contextsmanager.FromNodeAndID(nodeID, oclcontext)
            KernelProperties['Context'] = oclcontextID
        except:
            nErr = -128
            KernelProperties = {}
        return (KernelProperties, nErr)

    def CreateKernel(self, args):
        try:
            program = int(args['Program'])
            kernel_name = str(args['KernelName'])
            nodeID, progID = self.programsmanager.FromAlias(program)
            newargs = {'Program': progID, 'KernelName': kernel_name}
            respCreateKernel = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".kernels",
                                       method = 'CreateKernel',
                                       args = newargs)
            aliasID = self.Insert(nodeID, respCreateKernel[0])
        except:
            return -128
        return aliasID, respCreateKernel[1]

    def ReleaseKernel(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".kernels",
                                       method = 'ReleaseKernel',
                                       args = args)
            if result <= 0:
                self.Delete(nid)
        except:
            return -128
        return result

    def RetainKernel(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".kernels",
                                       method = 'RetainKernel',
                                       args = args)
        except:
            return -128
        return result

    def KernelSetArgument(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            paramIndex = int(args['ParamIndex'])
            body = args['ParamDict']
            paramDict = {}
            if body.has_key('LocalMemory'):
                paramDict = {'LocalMemory': int(body['LocalMemory'])}
            if body.has_key('DeviceMemoryObject'):
                memAliasID = int(body['DeviceMemoryObject'])
                memnodeID, memID = self.buffersmanager.FromAlias(memAliasID)
                if memnodeID != nodeID:
                    raise Exception("Kernel and memory object have to belong to the same node")
                paramDict = {'DeviceMemoryObject': memID}
            if body.has_key('HostValue'):
                base64string = str(body['HostValue'])
                paramDict = {'HostValue': str(body['HostValue'])}
            newargs = {'id': ID, 'ParamIndex': paramIndex, 'ParamDict': paramDict} 
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".kernels",
                                       method = 'KernelSetArgument',
                                       args = newargs)
        except:
            return -128
        return result


