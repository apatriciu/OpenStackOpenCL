from novaclient import extension
from novaclient.v1_1 import client
from novaclient.v1_1 import services
from novaclient import utils
from novaclient.v1_1.contrib import list_extensions
from novaclient.v1_1.contrib import openclcontexts
from novaclient.v1_1.contrib import opencldevices
from novaclient.v1_1.contrib import openclprograms
from novaclient.v1_1.contrib import openclbuffers
from novaclient.v1_1.contrib import openclkernels
from novaclient.v1_1.contrib import openclqueues
from binascii import unhexlify
from binascii import hexlify
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

def get_nova_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME'] 
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d

def GetOpenStackClient():
    creds = get_nova_creds()
    extensions = [
        extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
        extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
        extension.Extension(openclprograms.__name__.split(".")[-1], openclprograms),
        extension.Extension(openclbuffers.__name__.split(".")[-1], openclbuffers),
        extension.Extension(openclkernels.__name__.split(".")[-1], openclkernels),
        extension.Extension(openclqueues.__name__.split(".")[-1], openclqueues),
        ]
    return client.Client(http_log_debug = True, extensions=extensions, **creds)

kernelCode = """
__kernel void opticalflowkernel(__global int *image1, 
                                __global int *image2, 
                                int imagesize,
                                int windowsize,
                                // results
                                __global int *fx,
                                __global int *fy){
  // kernel for computing the optical flow
  // uses brute force; one thread per pixel
  // no shared memory
  // uses a window to compare the sum of squared differences
  // we use a rectangular grid with the same size as the image
  int row = get_global_id(1);
  int col = get_global_id(0);

  if(row > imagesize || col > imagesize) return;

  int bfirstconvolve = 1;
  float mincost = 1000000.0f;
  int frow = 0;
  int fcol = 0;
  int rw, cw, ii, jj, row_image1, row_image2, col_image1, col_image2;
  float cost;
  int val_image1;
  int val_image2;
  for(rw = -windowsize; rw <= windowsize; rw++)
    for(cw = -windowsize; cw <= windowsize; cw++){
      // compute the difference
      cost = 0.0f;
      for(ii = -windowsize; ii <= windowsize; ii++)
        for(jj = -windowsize; jj <= windowsize; jj++){
          row_image2 = row + rw + ii;
          col_image2 = col + cw + jj;
          row_image1 = row + ii;
          col_image1 = col + jj;
          val_image2 = (row_image2 >= 0 && row_image2 < imagesize && col_image2 >= 0 && col_image2 < imagesize) ?
                                                           image2[row_image2 * imagesize + col_image2] : 0;
          val_image1 = (row_image1 >= 0 && row_image1 < imagesize && col_image1 >= 0 && col_image1 < imagesize) ?
                                                           image1[row_image1 * imagesize + col_image1] : 0;
          cost = cost + (float)((val_image1 - val_image2)*(val_image1 - val_image2));
          }
      cost = cost / (float)((2 * windowsize + 1) * (2 * windowsize + 1));
      if(bfirstconvolve == 1){
        bfirstconvolve = 0;
        mincost = cost;
        frow = rw;
        fcol = cw;
        }
      else if(cost <= mincost){
	mincost = cost;
        frow = rw;
        fcol = cw;
        }
      }
  fy[row * imagesize + col] = frow;
  fx[row * imagesize + col] = fcol;
  return;
}
             """

def ImageFlowOpenCL(mat1, mat2, imagesize, kernelsize, deviceType):
    #if imagesize > 128:
    #    print "Maximum image size is 128"
    #    return [], []
    deviceIndex = 0
    blocksize = 16
    memorytransferslice = 16384
    if (imagesize % blocksize != 0):
        print "The image size should be a multiple of ", blocksize
        return [], []
    try:
        cl = GetOpenStackClient()
    except:
        print "Could not create the OpenStack client"
        return [], []
    lstDev = cl.opencldevices.list()
    if len(lstDev) == 0:
        print "No Devices Available"
        return [], []
    listDevices = [ lstDev[deviceIndex], ]
    propDevice = cl.opencldevices.show(listDevices[0])
    if propDevice.CL_ERROR_CODE != 0:
        print "Could not retrieve device properties"
        return [], []
    print "Device Name : ", propDevice.CL_DEVICE_NAME
    byteArrayMatrix1 = bytearray(IntArray2ByteArray(mat1, endianlittle = (propDevice.CL_DEVICE_ENDIAN_LITTLE == 1)))
    byteArrayMatrix2 = bytearray(IntArray2ByteArray(mat2, endianlittle = (propDevice.CL_DEVICE_ENDIAN_LITTLE == 1)))
    bytearrayImageSize = bytearray(Int2ByteArray(imagesize, endianlittle = (propDevice.CL_DEVICE_ENDIAN_LITTLE == 1)))
    bytearrayKernelSize = bytearray(Int2ByteArray(kernelsize, endianlittle = (propDevice.CL_DEVICE_ENDIAN_LITTLE == 1)))
    print "Creating OpenCL Context ..."
    contextProperties = []
    contextID, retErr = cl.openclcontexts.create(listDevices, contextProperties)
    if retErr != 0:
        print "Could not create the OpenCL context"
        return [], []
    print "Creating OpenCL Command Queue ..."
    queueCreateFlags = []
    queueID, retErr = cl.openclqueues.create(listDevices[0],
                                             contextID, 
                                             queueCreateFlags)
    if retErr != 0:
        print "Could not create the command queue"
        return [], []
    # create the 4 buffers
    bufferSize = len(byteArrayMatrix1)
    bufferCreateFlags = []
    bufferIDs = []
    print "Creating OpenCL Memory Buffers ..."
    for i in range(0, 4):
        bufImageID, retErr = cl.openclbuffers.create(contextID, bufferSize, bufferCreateFlags)
        if retErr != 0:
            print "Could not create the buffer"
            break
        bufferIDs.append( bufImageID )
    if len(bufferIDs) != 4:
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    # create the program and kernel
    # read the kernel file
    # fk = open('threadopticalflow.cl', 'r')
    # strKernel = fk.read()
    # fk.close()
    strKernel = kernelCode
    print "Creating OpenCL Programs ..."
    programID, retErr = cl.openclprograms.create(contextID, [strKernel,])
    if len(bufferIDs) != 4:
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    # try to build the program
    buildOptions = ""
    print "Compiling OpenCL Programs ..."
    retErr = cl.openclprograms.build(programID, listDevices, buildOptions)
    if retErr != 0:
        print "Build Error: "
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        dictResp, retErr = cl.openclprograms.buildinfo(programID, listDevices[0], buildInfo);
        print dictResp
        if dictResp["CL_PROGRAM_BUILD_STATUS"] != "CL_BUILD_SUCCESS":
            buildInfo = "CL_PROGRAM_BUILD_LOG"
            dictRest, retErr = cl.openclprograms.buildinfo(programID, listDevices[0], buildInfo);
            print dictRest
        cl.openclprograms.release(programID)
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    # create kernel
    print "Creating OpenCL Kernel ..."
    kernelID1, retErr = cl.openclkernels.create(programID, "opticalflowkernel")
    if retErr != 0:
        print "Create Kernel Error: "
        cl.openclprograms.release(programID)
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    # copy to memory
    print "Copying Data from Host to OpenCL Device Memory..."
    startSlice = 0
    while startSlice < bufferSize:
        endSlice = startSlice + memorytransferslice
        if endSlice > bufferSize:
            endSlice = bufferSize
        dataSlice = byteArrayMatrix1[startSlice : endSlice]
        nBytes = endSlice - startSlice
        retErr = cl.openclqueues.enqueuewritebuffer(queue_id = queueID, 
                                                    buffer_id = bufferIDs[0],
                                                    ByteCount = nBytes, 
                                                    Offset = startSlice, 
                                                    data = dataSlice)
        startSlice = endSlice
        if retErr != 0:
            break
    if retErr != 0:
        print "EnqueueWriteBuffer Error"
        cl.openclkernels.release(KernelID)
        cl.openclprograms.release(programID)
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    startSlice = 0
    while startSlice < bufferSize:
        endSlice = startSlice + memorytransferslice
        if endSlice > bufferSize:
            endSlice = bufferSize
        dataSlice = byteArrayMatrix2[startSlice : endSlice]
        nBytes = endSlice - startSlice
        retErr = cl.openclqueues.enqueuewritebuffer(queue_id = queueID, 
                                                buffer_id = bufferIDs[1],
                                                ByteCount = nBytes, 
                                                Offset = startSlice, 
                                                data = dataSlice)
        startSlice = endSlice
        if retErr != 0:
            break
    if retErr != 0:
        print "EnqueueWriteBuffer Error"
        cl.openclkernels.release(KernelID)
        cl.openclprograms.release(programID)
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    # set kernel parameters
    dictParamsKernel = {0 : {'DeviceMemoryObject': bufferIDs[0]},
                        1 : {'DeviceMemoryObject': bufferIDs[1]},
                        2 : {'HostValue': bytearrayImageSize},
                        3 : {'HostValue': bytearrayKernelSize},
                        4 : {'DeviceMemoryObject': bufferIDs[2]},
                        5 : {'DeviceMemoryObject': bufferIDs[3]}}
    for indexParam, dictParamValue in dictParamsKernel.iteritems():
        retErr = cl.openclkernels.setkernelarg(kernelID1, indexParam, 
                                               dictParamValue.items()[0][0], 
                                               dictParamValue.items()[0][1])
        if retErr != 0:
            print "Kernel Set Params Error"
            print "indexParam : ", indexParam, "; Error : ", retErr
            cl.openclkernels.release(kernelID1)
            cl.openclprograms.release(programID)
            for buf in bufferIDs:
                cl.openclbuffers.release(buf)
            cl.openclqueues.release(queueID)
            cl.openclcontexts.release(contextID)
            return [], [] 
    globalOffset = [0, 0]
    globalworksize = [imagesize, imagesize]
    localworksize = [blocksize, blocksize] 
    print "Launching ND Range Kernel ..."
    # launch kernel
    retErr = cl.openclqueues.enqueuendrangekernel(queue_id = queueID, 
                                                  kernel_id = kernelID1, 
                                                  global_offset = globalOffset, 
                                                  global_size = globalworksize, 
                                                  local_size = localworksize);
    if retErr != 0:
        print "EnqueueNDRangeKernel Error : ", retErr
        cl.openclkernels.release(kernelID1)
        cl.openclprograms.release(programID)
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    # read the result
    print "Copying Results from OpenCL Device Memory to Host Memory ..."
    fx = ""
    startSlice = 0
    while startSlice < bufferSize:
        print "Copying Buffer 2: startSlice ", startSlice
        endSlice = startSlice + memorytransferslice
        if endSlice > bufferSize:
            endSlice = bufferSize
        nBytes = endSlice - startSlice
        dataSlice, retErr = cl.openclqueues.enqueuereadbuffer(queue_id = queueID, 
                                                       buffer_id = bufferIDs[2], 
                                                       ByteCount = nBytes,
                                                       Offset = startSlice)
        startSlice = endSlice
        if retErr != 0:
            break
        fx += dataSlice
    if retErr != 0:
        print "EnqueueReadBuffer Error; retErr : ", retErr
        cl.openclkernels.release(kernelID1)
        cl.openclprograms.release(programID)
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    flowx = bytearray(fx)
    fy = ""
    startSlice = 0
    while startSlice < bufferSize:
        print "Copying Buffer 3: startSlice ", startSlice
        endSlice = startSlice + memorytransferslice
        if endSlice > bufferSize:
            endSlice = bufferSize
        nBytes = endSlice - startSlice
        dataSlice, retErr = cl.openclqueues.enqueuereadbuffer(queue_id = queueID,
                                                       buffer_id = bufferIDs[3], 
                                                       ByteCount = nBytes,
                                                       Offset = startSlice)
        startSlice = endSlice
        if retErr != 0:
            break
        fy += dataSlice
    if retErr != 0:
        print "EnqueueReadBuffer Error; retErr : ", retErr
        cl.openclkernels.release(kernelID1)
        cl.openclprograms.release(programID)
        for buf in bufferIDs:
            cl.openclbuffers.release(buf)
        cl.openclqueues.release(queueID)
        cl.openclcontexts.release(contextID)
        return [], []
    flowy = bytearray(fy)
    # convert to ints
    listflowx = ByteArray2IntArray(flowx)
    listflowy = ByteArray2IntArray(flowy)
    cl.openclkernels.release(kernelID1)
    cl.openclprograms.release(programID)
    for buf in bufferIDs:
        cl.openclbuffers.release(buf)
    cl.openclqueues.release(queueID)
    cl.openclcontexts.release(contextID)
    return listflowx, listflowy    

if __name__ == "__main__":
    imagesize = 64
    kernelsize = 3
    dx = 1
    dy = 1
    mat1 = getRandomMatrix(imagesize)
    mat2 = ShiftImage(mat1, imagesize, dx, dy)
    #print "Mat Input : ", mat
    for ii in range(0, 1):
        print " --------------- Run # ", ii, " ---------------------"
        resMat1, resMat2 = ImageFlowOpenCL(mat1, mat2, 
                                 imagesize, kernelsize, "GPU")
    #print "Mat Output : ", resMat
    #print "resMat1 = ", resMat1
    #print "resMat2 = ", resMat2
    print "Done : "

