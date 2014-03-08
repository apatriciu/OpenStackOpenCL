from swiftclient import client as cs

def credentials():
    creds = {}
    creds['authurl'] = os.environ["OS_AUTH_URL"]
    creds['username'] = os.environ["OS_USERNAME"]
    creds['password'] = os.environ["OS_PASSWORD"]
    creds['tenant_name'] = os.environ['OS_TENANT_NAME']
    return creds

class SwiftUtils(object):
    def __init__(self):
        creds = credentials()
        self.swifturl, self.swifttoken = cs.get_keystoneclient_2_0( auth_url = creds['authurl'],
                             user = creds['username'],
                             key = creds['password'],
                             {'tenant_name': creds['tenant_name']})
    def createcontainer(self, name):
        cs.put_container(url = self.swifturl, 
                         token = self.swifttoken,
                         container = name )

    def createobject(self, objectname, objectdata, container):
        data_length = len(objectdata)
        cs.put_object(url = self.swifturl, 
                      token = self.swifttoken,
                      container = container,
                      name = objectname,
                      contents = objectdata,
                      content_length = data_length)

    def getobjectdata(self, objectname, container):
        respdict, respobj = cs.get_object( url = self.swifturl,
                                           token = self.swifttoken, 
                                           container = container,
                                           name = objectname)
        return respobj

    def deleteobject(self, container, objectname):
        cs.delete_object(url = self.swifturl, 
                      token = self.swifttoken,
                      container = container,
                      name = objectname)

    def deletecontainer(self, container):
        cs.delete_container(url = self.swifturl, 
                      token = self.swifttoken,
                      container = container)

    def getcontext(self):
        creds = {}
        creds['UserName'] = os.environ["OS_USERNAME"]
        creds['Password'] = os.environ["OS_PASSWORD"]
        creds['TenantName'] = os.environ['OS_TENANT_NAME']
        return creds


