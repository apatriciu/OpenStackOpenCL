import unittest
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager

class TestOCLResourceAliasManager(unittest.TestCase):
    oram = OpenCLResourcesAliasManager()

    def testInsertNew(self):
        nodeID = "ASDFGH"
        ID = 0
        aliasID = self.oram.Insert(nodeID, ID)
        # retrieve the data
        (retnodeID, retID) = self.oram.FromAlias(aliasID)
        self.assertEqual(ID, retID)
        self.assertEqual(nodeID, retnodeID)
        # delete the entry
        self.oram.Delete(aliasID)

    def testInverseMap(self):
        nodeID = "ASDFGH"
        ID = 0
        aliasID = self.oram.Insert(nodeID, ID)
        # retrieve the data
        retaliasID = self.oram.FromNodeAndID(nodeID, ID)
        self.assertEqual(retaliasID, aliasID)
        # delete the entry
        self.oram.Delete(aliasID)

    def testInvalidCombination(self):
        nodeID = "qwerty"
        ID = 1
        aliasID = 100
        self.assertRaises(Exception, self.oram.FromNodeAndID, nodeID, ID)
        self.assertRaises(Exception, self.oram.FromAlias, aliasID)

if __name__ == "__main__":
    unittest.main()

