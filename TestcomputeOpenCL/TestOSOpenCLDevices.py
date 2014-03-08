# test OpenCL extension for nova compute service

from openclclient import client

cl = client.Client()

# check openclinterface list
listdevices = cl.opencldevices.list()
print("List devices", listdevices)

device_id = 0
device_info = cl.opencldevices.show(device_id)
print "Device ID : ", device_info.id
print "Device Name: ", device_info.CL_DEVICE_NAME

