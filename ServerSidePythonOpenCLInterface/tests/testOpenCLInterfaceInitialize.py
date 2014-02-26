import unittest
import PyOpenCLInterface

class TestInitSystem(unittest.TestCase):
    def testInitialize(self):
        """Test Initialize"""
        retVal = PyOpenCLInterface.Initialize("GPU");
        self.assertEqual(retVal, 0)

if __name__ == "__main__":
    unittest.main()

