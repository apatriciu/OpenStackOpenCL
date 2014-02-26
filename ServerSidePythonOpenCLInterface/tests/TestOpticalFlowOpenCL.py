from binascii import unhexlify
from binascii import hexlify
import PyOpenCLInterface
import random

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

def Int2ByteArray(intval, endianlittle = True):
    # we assume that intval is an integer that can be represented on 4 bytes
    strIntValHex = "%08x" % intval
    ba = unhexlify(strIntValHex)
    if endianlittle:
        ba = ba[::-1]
    return ba

def ByteArray2Int(bytearrayval, endianlittle = True):
    # the bytearray should have exactly 4 bytes
    if endianlittle:
        bytearrayval = bytearrayval[::-1]
    hexarray = hexlify(bytearrayval)
    return int("0x" + hexarray)

def ShiftImage(inputimage, size, dx, dy):
    outputimage = list(range(0, size * size))
    for row in range(0, size):
        for col in range(0, size):
            if (row - dy >= 0) and (row - dy < size) and (col - dx >= 0) and (col - dx < size):
                outputimage[row*size + col] = inputimage[(row - dy)*size + col - dx]
            else:
                outputimage[row*size + col] = 0
    return outputimage

def ImageFlowOpenCL(mat1, mat2, imagesize, kernelsize, deviceType):
    deviceIndex = 0
    blocksize = 4
    retErr = PyOpenCLInterface.Initialize(deviceType)
    if retErr != 0:
        print "Interface Initialization Error"
        return [],[]
    lstDev, retErr = PyOpenCLInterface.ListDevices()
    if len(lstDev) == 0:
        print "No Devices Available"
        return [], []
    listDevices = [ lstDev[deviceIndex], ]
    propDevice, retErr = PyOpenCLInterface.GetDeviceProperties(listDevices[0])
    if retErr != 0:
        print "Could not retrieve device properties"
        return [], []
    print "Device Name : ", propDevice['CL_DEVICE_NAME']
    byteArrayMatrix1 = bytearray(IntArray2ByteArray(mat1, endianlittle = (propDevice['CL_DEVICE_ENDIAN_LITTLE'] == 1)))
    byteArrayMatrix2 = bytearray(IntArray2ByteArray(mat2, endianlittle = (propDevice['CL_DEVICE_ENDIAN_LITTLE'] == 1)))
    bytearrayImageSize = bytearray(Int2ByteArray(imagesize, endianlittle = (propDevice['CL_DEVICE_ENDIAN_LITTLE'] == 1)))
    bytearrayKernelSize = bytearray(Int2ByteArray(kernelsize, endianlittle = (propDevice['CL_DEVICE_ENDIAN_LITTLE'] == 1)))
    contextProperties = {}
    contextID, retErr = PyOpenCLInterface.CreateContext(listDevices, contextProperties)
    if retErr != 0:
        print "Could not create the OpenCL context"
        return [], []
    queueCreateFlags = []
    queueID, retErr = PyOpenCLInterface.CreateQueue(contextID,
                                                    listDevices[0], 
                                                    queueCreateFlags)
    if retErr != 0:
        print "Could not create the command queue"
        return [], []
    # create the 4 buffers
    bufferSize = len( byteArrayMatrix1)
    bufferCreateFlags = []
    bufferIDs = []
    for i in range(0, 4):
        bufImageID, retErr = PyOpenCLInterface.CreateBuffer(contextID, bufferSize, bufferCreateFlags)
        if retErr != 0:
            print "Could not create the buffer"
            break
        bufferIDs.append( bufImageID )
    if len(bufferIDs) != 4:
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    # create the program and kernel
    # read the kernel file
    fk = open('threadopticalflow.cl', 'r')
    strKernel = fk.read()
    fk.close()
    programID, retErr = PyOpenCLInterface.CreateProgram(contextID, [strKernel,])
    if len(bufferIDs) != 4:
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    # try to build the program
    buildOptions = ""
    retErr = PyOpenCLInterface.BuildProgram(programID, listDevices, buildOptions)
    if retErr != 0:
        print "Build Error: "
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        dictResp, retErr = PyOpenCLInterface.GetProgramBuildInfo(programID, listDevices[0], buildInfo);
        print dictResp
        if dictResp["CL_PROGRAM_BUILD_STATUS"] != "CL_BUILD_SUCCESS":
            buildInfo = "CL_PROGRAM_BUILD_LOG"
            dictRest, retErr = PyOpenCLInterface.GetProgramBuildInfo(programID, listDevices[0], buildInfo);
            print dictRest
        PyOpenCLInterface.ReleaseProgram(programID)
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    # create kernel
    kernelID1, retErr = PyOpenCLInterface.CreateKernel(programID, "opticalflowkernel")
    if retErr != 0:
        print "Create Kernel Error: "
        PyOpenCLInterface.ReleaseProgram(programID)
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    # copy to memory
    retErr = PyOpenCLInterface.EnqueueWriteBuffer(queueID, bufferIDs[0],
                                                  bufferSize, 0, byteArrayMatrix1)
    if retErr != 0:
        print "EnqueueWriteBuffer Error"
        PyOpenCLInterface.ReleaseKernel(KernelID)
        PyOpenCLInterface.ReleaseProgram(programID)
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    retErr = PyOpenCLInterface.EnqueueWriteBuffer(queueID, bufferIDs[1],
                                                  bufferSize, 0, byteArrayMatrix2)
    if retErr != 0:
        print "EnqueueWriteBuffer Error"
        PyOpenCLInterface.ReleaseKernel(KernelID)
        PyOpenCLInterface.ReleaseProgram(programID)
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    # set kernel parameters
    dictParamsKernel = {0 : {'DeviceMemoryObject': bufferIDs[0]},
                        1 : {'DeviceMemoryObject': bufferIDs[1]},
                        2 : {'HostValue': bytearrayImageSize},
                        3 : {'HostValue': bytearrayKernelSize},
                        4 : {'DeviceMemoryObject': bufferIDs[2]},
                        5 : {'DeviceMemoryObject': bufferIDs[3]}}
    for indexParam, dictParamValue in dictParamsKernel.iteritems():
        retErr = PyOpenCLInterface.KernelSetArgument(kernelID1, indexParam, dictParamValue)
        if retErr != 0:
            print "Kernel Set Params Error"
            print "indexParam : ", indexParam, "; Error : ", retErr
            PyOpenCLInterface.ReleaseKernel(kernelID1)
            PyOpenCLInterface.ReleaseProgram(programID)
            for buf in bufferIDs:
                PyOpenCLInterface.ReleaseBuffer(buf)
            PyOpenCLInterface.ReleaseQueue(queueID)
            PyOpenCLInterface.ReleaseContext(contextID)
            return [], [] 
    globalOffset = [0, 0]
    globalworksize = [imagesize, imagesize]
    localworksize = [blocksize, blocksize]
    # launch kernel
    retErr = PyOpenCLInterface.EnqueueNDRangeKernel(queueID, kernelID1, globalOffset, globalworksize, localworksize);
    if retErr != 0:
        print "EnqueueNDRangeKernel Error : ", retErr
        PyOpenCLInterface.ReleaseKernel(kernelID1)
        PyOpenCLInterface.ReleaseProgram(programID)
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    # read the result
    flowx, retErr1 = PyOpenCLInterface.EnqueueReadBuffer(queueID, bufferIDs[2], bufferSize, 0)
    flowy, retErr2 = PyOpenCLInterface.EnqueueReadBuffer(queueID, bufferIDs[3], bufferSize, 0)
    if retErr1 != 0 or retErr2 != 0:
        print "EnqueueReadBuffer Error; retErr1 : ", retErr1, "; retErr2 : ", retErr2 
        PyOpenCLInterface.ReleaseKernel(kernelID1)
        PyOpenCLInterface.ReleaseProgram(programID)
        for buf in bufferIDs:
            PyOpenCLInterface.ReleaseBuffer(buf)
        PyOpenCLInterface.ReleaseQueue(queueID)
        PyOpenCLInterface.ReleaseContext(contextID)
        return [], []
    print bufferSize
    # convert to ints
    listflowx = ByteArray2IntArray(flowx)
    listflowy = ByteArray2IntArray(flowy)
    PyOpenCLInterface.ReleaseKernel(kernelID1)
    PyOpenCLInterface.ReleaseProgram(programID)
    for buf in bufferIDs:
        PyOpenCLInterface.ReleaseBuffer(buf)
    PyOpenCLInterface.ReleaseQueue(queueID)
    PyOpenCLInterface.ReleaseContext(contextID)
    return listflowx, listflowy    

if __name__ == "__main__":
    imagesize = 64
    kernelsize = 2
    dx = 1
    dy = 1
    mat1 = getRandomMatrix(imagesize)
    mat2 = ShiftImage(mat1, imagesize, dx, dy)
    #print "Mat Input : ", mat
    resMat1, resMat2 = ImageFlowOpenCL(mat1, mat2, imagesize, kernelsize, "GPU")
    #print "Mat Output : ", resMat
    #print "resMat1 = ", resMat1
    #print "resMat2 = ", resMat2
    print "Done : "

