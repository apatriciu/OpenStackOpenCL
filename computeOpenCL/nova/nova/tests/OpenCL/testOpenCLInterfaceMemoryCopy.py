import unittest
from nova.OpenCL import OpenCLContextsAPI
from nova.OpenCL import OpenCLClientException
from nova.OpenCL import OpenCLCommandQueuesAPI
from nova.OpenCL import OpenCLBuffersAPI
import sys
import binascii
from binascii import unhexlify
from binascii import hexlify
import random


class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    device_type = "GPU"

class TestQueuesMemCopy(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    contexts_interface = OpenCLContextsAPI.API()
    buffers_interface = OpenCLBuffersAPI.API()
    command_queues_interface = OpenCLCommandQueuesAPI.API()

    def setUp(self):
        self.contextID, retErr = self.contexts_interface.CreateContext(self.testResources.listDevicesIDs, 
                                                    self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueCreateFlags = []
        self.queueID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                                                    self.testResources.listDevicesIDs[0], 
                                                    queueCreateFlags)
        self.assertEqual(retErr, 0)
        self.RawString = bytearray("11111111")
        self.base64EncodedString = str(binascii.b2a_base64(self.RawString))
        self.bufferSize = len(self.RawString)
        bufferCreateFlags = []
        self.bufferID, retErr = self.buffers_interface.CreateBuffer(self.contextID, 
                                                    self.bufferSize, 
                                                    bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.bufferID2, retErr = self.buffers_interface.CreateBuffer(self.contextID, 
                                                    self.bufferSize, 
                                                    bufferCreateFlags)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferID)
        self.assertEqual(retErr, 0)
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferID2)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.ReleaseQueue(self.queueID)
        self.assertEqual(retErr, 0)
        retErr = self.contexts_interface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)

    def testWriteAndRead(self):
        # copy to the device memory
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 
                                                    0, 
                                                    self.base64EncodedString)
        self.assertEqual(retErr, 0)
        retData, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 0)
        # decode
        rawRetData = binascii.a2b_base64(str(retData))
        self.assertEqual(len(rawRetData), self.bufferSize)
        self.assertEqual(retErr, 0)
        self.assertEqual(rawRetData, self.RawString)

    def testWriteCopyRead(self):
        # copy to the device memory
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 
                                                    0, 
                                                    self.base64EncodedString)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.EnqueueCopyBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferID2, 
                                                    self.bufferSize, 
                                                    0, 0)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.EnqueueBarrier(self.queueID)
        self.assertEqual(retErr, 0)
        retData, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                                    self.bufferID2, self.bufferSize, 0)
        # decode
        rawRetData = binascii.a2b_base64(str(retData))
        self.assertEqual(len(rawRetData), self.bufferSize)
        self.assertEqual(retErr, 0)
        self.assertEqual(rawRetData, self.RawString)

def getRandomMatrix(sizeImage):
    retVal = list(range(0, sizeImage*sizeImage))
    for indexelem in range(0, sizeImage*sizeImage):
        retVal[indexelem] = random.randint(0, 4096)
    return retVal

def ByteArray2IntArray(imageByteArray, endianlittle = True):
    # we have 4 bytes per integer
    nElems = len(imageByteArray) / 4
    imageintarray = list(range(0, nElems))
    for indexElem in range(0, nElems):
        startPos = indexElem * 4
        endPos = (indexElem + 1) * 4
        ba = imageByteArray[startPos : endPos]
        if endianlittle:
            ba = ba[::-1]
        hexba = hexlify(ba)
        imageintarray[indexElem] = int("0x" + hexba, base = 0)
        if imageintarray[indexElem] > 0x7FFFFFFF:
            imageintarray[indexElem] -= 0x100000000
            #imageintarray[indexElem] = -imageintarray[indexElem]
    return imageintarray

def IntArray2ByteArray(image, endianlittle = True):
    # the image is sizeImage x sizeImage pixel values
    # each pixel is an integer represented on 4 Bytes

    byteArrayMatrix = ""
    for pixel in image:
        # we need eight hexadecimal digits for one integer
        s = "%08x" % pixel
        ba = unhexlify( s )
        if endianlittle:
            ba = ba[::-1]
        byteArrayMatrix = byteArrayMatrix + ba
    return byteArrayMatrix

class TestQueuesLargeMemCopy(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    contexts_interface = OpenCLContextsAPI.API()
    buffers_interface = OpenCLBuffersAPI.API()
    command_queues_interface = OpenCLCommandQueuesAPI.API()

    def setUp(self):
        self.contextID, retErr = self.contexts_interface.CreateContext(self.testResources.listDevicesIDs, 
                                                    self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueCreateFlags = []
        self.queueID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                                                    self.testResources.listDevicesIDs[0], 
                                                    queueCreateFlags)
        self.assertEqual(retErr, 0)
        self.matrixsize = 256
        self.sourceMatrix = getRandomMatrix(self.matrixsize)
        self.RawString = bytearray( IntArray2ByteArray(self.sourceMatrix) )
        self.bufferSize = len(self.RawString)
        # RawString is a byte array of length ByteCount; We have to divide 
        # RawString in 57 bytes slices and convert to base64
        Data = ""
        StartPosition = 0
        while StartPosition < self.bufferSize:
            EndPosition = StartPosition + 57
            if EndPosition > self.bufferSize:
                EndPosition = self.bufferSize
            Data2Convert = bytearray(self.RawString[StartPosition : EndPosition])
            StartPosition = EndPosition
            base64Data = binascii.b2a_base64(Data2Convert)
            Data = Data + base64Data
        self.base64EncodedString = str(Data)
        bufferCreateFlags = []
        self.bufferID, retErr = self.buffers_interface.CreateBuffer(self.contextID, 
                                                    self.bufferSize, 
                                                    bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.bufferID2, retErr = self.buffers_interface.CreateBuffer(self.contextID, 
                                                    self.bufferSize, 
                                                    bufferCreateFlags)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferID)
        self.assertEqual(retErr, 0)
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferID2)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.ReleaseQueue(self.queueID)
        self.assertEqual(retErr, 0)
        retErr = self.contexts_interface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)

    def testWriteAndRead(self):
        # copy to the device memory
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 
                                                    0, 
                                                    self.base64EncodedString)
        self.assertEqual(retErr, 0)
        retData, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 0)
        # decode
        rawRetData = binascii.a2b_base64(str(retData))
        self.assertEqual(len(rawRetData), self.bufferSize)
        self.assertEqual(retErr, 0)
        self.assertEqual(rawRetData, self.RawString)

    def testWriteCopyRead(self):
        # copy to the device memory
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferSize, 
                                                    0, 
                                                    self.base64EncodedString)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.EnqueueCopyBuffer(self.queueID, 
                                                    self.bufferID, 
                                                    self.bufferID2, 
                                                    self.bufferSize, 
                                                    0, 0)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.EnqueueBarrier(self.queueID)
        self.assertEqual(retErr, 0)
        retData, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                                    self.bufferID2, self.bufferSize, 0)
        # decode
        rawRetData = binascii.a2b_base64(str(retData))
        self.assertEqual(len(rawRetData), self.bufferSize)
        self.assertEqual(retErr, 0)
        self.assertEqual(rawRetData, self.RawString)

if __name__ == "__main__":
    unittest.main()

