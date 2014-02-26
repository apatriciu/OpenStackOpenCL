# test OpenCL extension for nova compute service

from novaclient import extension
from novaclient.v1_1 import client
from novaclient.v1_1 import services
from novaclient import utils
from novaclient.v1_1.contrib import list_extensions
from novaclient.v1_1.contrib import opencldevices
from credentials import get_nova_creds

creds = get_nova_creds()
extensions = [
    extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
    ]
cl = client.Client(http_log_debug = True, extensions=extensions, **creds)

# check openclinterface list
listdevices = cl.opencldevices.list()
print("List devices", listdevices)

device_id = 0
device_info = cl.opencldevices.show(device_id)
print "Device ID : ", device_info.id
print "Device Name: ", device_info.CL_DEVICE_NAME

