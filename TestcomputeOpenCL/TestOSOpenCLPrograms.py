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

from credentials import get_nova_creds

creds = get_nova_creds()
extensions = [
    extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
    extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
    extension.Extension(openclprograms.__name__.split(".")[-1], openclprograms),
    ]
cl = client.Client(http_log_debug = True, extensions=extensions, **creds)

print "Create a Context: "
devices = [0, ]
properties = []
context, retErr = cl.openclcontexts.create(devices, properties)
print("ContextID : ", context)
print("retErr : ", retErr)

print("create program")
programcode = ["__kernel void dummy(int a){ int ii = a; }",]
program_id, retErr = cl.openclprograms.create(context, programcode)
print("Program ID : ", program_id)
print("retErr : ", retErr)

print("list programs")
# check openclprogramsinterface list
ocprograms = cl.openclprograms.list()
print(ocprograms)

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
print("Build Info : ", buildInfo)
print("retErr : ", retErr)

print("release program")
retErr = cl.openclprograms.release(program_id)
print("retErr : ", retErr)

print "Release the Context: "
retErr = cl.openclcontexts.release(context)
print("retErr : ", retErr)

