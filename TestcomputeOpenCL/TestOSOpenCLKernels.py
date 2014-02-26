# test OpenCL extension for nova compute service

import math

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

from credentials import get_nova_creds

creds = get_nova_creds()
extensions = [
    extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
    extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
    extension.Extension(openclprograms.__name__.split(".")[-1], openclprograms),
    extension.Extension(openclbuffers.__name__.split(".")[-1], openclbuffers),
    extension.Extension(openclkernels.__name__.split(".")[-1], openclkernels),
    ]
cl = client.Client(http_log_debug = True, extensions=extensions, **creds)

print "Create a Context: "
devices = [0, ]
properties = []
context, retErr = cl.openclcontexts.create(devices, properties)
print("Context ID:", context)
print("retErr : ", retErr)

print("create program")
programcode = ["__kernel void dummy(int a, __global float* b, __local float* sha){ int ii = a; }",]
program_id, retErr = cl.openclprograms.create(context, programcode)
print("Program ID : ", program_id)
print("retErr : ", retErr)

print("list programs")
# check openclprogramsinterface list
listprograms = cl.openclprograms.list()
print("List Programs : ", listprograms)

print("show program")
oc_program = cl.openclprograms.show(program_id)
print(oc_program)

print("build program")
build_options = ""
retErr = cl.openclprograms.build(program_id, devices, build_options)
print("retErr : ", retErr)

print("buildinfo program")
buildinfo_param = 'CL_PROGRAM_BUILD_STATUS'
buildInfo, retErr = cl.openclprograms.buildinfo(program_id, devices[0], buildinfo_param)
print("Build Info: ", buildInfo)
print("retErr : ", retErr)

print("create Buffer")
size = 256
properties = []
buffer_id, retErr = cl.openclbuffers.create(context, size, properties)
print("buffer ID : ", buffer_id)
print("retErr : ", retErr)

print("create the Kernel")
kernel_function_name = "dummy"
kernel_id, retErr = cl.openclkernels.create(program_id, kernel_function_name)
print("Kernel ID : ", kernel_id)
print("retErr : ", retErr)

print("Show Program Properties")
oc_kernel = cl.openclkernels.show(0)
print oc_kernel

print("Set argument 0")
byteArrayParam = bytearray( '1111' )
argIndex = 0
retErr = cl.openclkernels.setkernelarg(kernel_id, argIndex, 'HostValue', byteArrayParam)
print("retErr : ", retErr)
 
print("Set argument 1")
argIndex = 1
retErr = cl.openclkernels.setkernelarg(kernel_id, argIndex, 'DeviceMemoryObject', buffer_id)
print("retErr : ", retErr)
 
print("Set argument 2")
argIndex = 2
retErr = cl.openclkernels.setkernelarg(kernel_id, argIndex, 'LocalMemory', 64)
print("retErr : ", retErr)

print("List Kernels")
list_kernels = cl.openclkernels.list()
print list_kernels

print("Release the kernel")
retErr = cl.openclkernels.release(kernel_id)
print("retErr : ", retErr)

print("List Kernels")
list_kernels = cl.openclkernels.list()
print("List Kernels : ", list_kernels)

print("release program")
retErr = cl.openclprograms.release(program_id)
print("retErr : ", retErr)

print("release Buffer")
retErr = cl.openclbuffers.release(buffer_id)
print("retErr : ", retErr)

print "Release the Context: "
retErr = cl.openclcontexts.release(context)
print("retErr : ", retErr)

