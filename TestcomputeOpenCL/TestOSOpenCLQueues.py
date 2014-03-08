# test OpenCL extension for nova compute service

import math
from openclclient import client

cl = client.Client()

print "Create a Context: "
devices = [0, ]
properties = []
context, retVal = cl.openclcontexts.create(devices, properties)
print("Context ID : ", context)
print("retVal : ", retVal)
device = devices[0]

print("create the queue")
properties = []
queue_id, retVal = cl.openclqueues.create(device, context, properties)
print "Queue ID : ", queue_id
print("retVal : ", retVal)

command_queue_created = True
if retVal != 0: 
    print 'Failed to allocate execution queue resources'
    command_queue_created = False
    
print("create program")
programcode = ['''__kernel void kernel2(int a, __global int *b, __local int *sh){
                     sh[0] = a;
                     b[get_global_id(0)] = sh[0];
                  }
               ''',]

program_id, retVal = cl.openclprograms.create(context, programcode)
print("Program ID : ", program_id)
print("retVal : ", retVal)


print("list programs")
# check openclprogramsinterface list
ocprograms = cl.openclprograms.list()
print(ocprograms)

print("show program")
oc_program = cl.openclprograms.show(program_id)
print(oc_program)

print("build program")
build_options = ""
retVal = cl.openclprograms.build(program_id, devices, build_options)
print("retVal : ", retVal)

print("buildinfo program")
buildinfo_param = 'CL_PROGRAM_BUILD_STATUS'
buildinfo, retVal = cl.openclprograms.buildinfo(program_id, devices[0], buildinfo_param)
print("retVal : ", retVal)
print("Build Info : ", buildinfo)

print("create Buffer")
size = 256
properties = []
buffer_id, retVal = cl.openclbuffers.create(context, size, properties)
print("Buffer ID : ", buffer_id)
print("retVal : ", retVal)

print("create the Kernel")
kernel_function_name = "kernel2"
kernel_id, retVal = cl.openclkernels.create(program_id, kernel_function_name)
print "Kernel ID : ", kernel_id
print("retVal : ", retVal)

print("Show kernel Properties")
oc_kernel = cl.openclkernels.show(kernel_id)
print oc_kernel

print("Set argument 0")
byteArrayParam = bytearray( '1243' )
argIndex = 0
retVal = cl.openclkernels.setkernelarg(kernel_id, argIndex, 'HostValue', byteArrayParam)
print("retVal : ", retVal)
 
print("Set argument 1")
argIndex = 1
retVal = cl.openclkernels.setkernelarg(kernel_id, argIndex, 'DeviceMemoryObject', buffer_id)
print("retVal : ", retVal)
 
print("Set argument 2")
argIndex = 2
retVal = cl.openclkernels.setkernelarg(kernel_id, argIndex, 'LocalMemory', 64)
print("retVal : ", retVal)

print("List Kernels")
list_kernels = cl.openclkernels.list()
print list_kernels

if command_queue_created:
    print("Launch the kernel")
    gwsz = [2,]
    gwo = [0,]
    lwsz = [2,]
    retVal = cl.openclqueues.enqueuendrangekernel(queue_id=queue_id, kernel_id=kernel_id,
                                           global_size=gwsz, global_offset=gwo,
                                                local_size=lwsz)
    print("retVal : ", retVal)

    print("Copy back the result")
    Data, retVal = cl.openclqueues.enqueuereadbuffer(queue_id=queue_id, buffer_id=buffer_id, ByteCount = 8)
    print("retVal : ", retVal)
    print "Data : ", Data

print("Release the kernel")
retVal = cl.openclkernels.release(kernel_id)
print("retVal : ", retVal)

print("List Kernels")
list_kernels = cl.openclkernels.list()
print list_kernels

print("release program")
retVal = cl.openclprograms.release(program_id)
print("retVal : ", retVal)

print("release Buffer")
retVal = cl.openclbuffers.release(buffer_id)
print("retVal : ", retVal)

if command_queue_created:
    print("release the queue")
    retVal = cl.openclqueues.release(queue_id)
    print("retVal : ", retVal)

print "Release the Context: "
retVal = cl.openclcontexts.release(context)
print("retVal : ", retVal)

