
class OpenCLResourcesAliasManager(object):

    class OpenCLResource(object):
        def __init__(self, 
                     aliasID, # external id
                     nodeID, # the node on which the resource resides
                     ID): # the id on the node
            self.ID = ID
            self.aliasID = aliasID
            self.nodeID = nodeID

    max_resources_index = 100000

    def __init__(self):
        self.map_resources = {}

    def Insert(self, nodeID, ID):
        # find the first alias that is not present in the 
        # dictionary
        aliasID = 0
        while aliasID in self.map_resources:
            aliasID += 1
            if aliasID > self.max_resources_index:
                raise Exception("Out of resources")
        self.map_resources[aliasID] = self.OpenCLResource(aliasID, 
                                                          nodeID,
                                                          ID)
        return aliasID

    def FromAlias(self, aliasID):
        res = self.map_resources[aliasID]
        return (res.nodeID, res.ID)

    def FromNodeAndID(self, nodeID, ID):
        for k, v in self.map_resources.iteritems():
            if (v.ID == ID) and (v.nodeID == nodeID):
                return k
        raise Exception("Invalid combination node and key")

    def Delete(self, aliasID):
        if aliasID in self.map_resources:
            del self.map_resources[aliasID]

    def DeleteNodeResources(self, nodeID):
        listKeys2Delete = []
        for k, v in self.map_resources.iteritems():
            if v.nodeID == nodeID:
                listKeys2Delete.append( k )
        for k in listKeys2Delete:
            del self.map_resources[k]

    def List(self, args = None):
        return self.map_resources.keys()

