# vim: tabstop=4 shiftwidth=4 softtabstop=4

# OpenCL interface for OpenStack
# This file contains utility classes used by other modules

from nova.api.openstack import xmlutil

#XML Builder for ERROR_CODE response
class OpenCLErrorResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ErrorOnlyResponseTemplate')
        element = xmlutil.SubTemplateElement(root, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder forcreate(...) resp
class CreateResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('NewResourceItem')
        element = xmlutil.SubTemplateElement(root, 'CreateResp')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        subelement = xmlutil.SubTemplateElement(element, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

