from os import pread
from json import JSONEncoder

class ServiceMethodEntity:   


    def __init__(self, prefix ):
        self.name = None
        self.tags = list()
        self.service_id = None
        self.service = None
        self.method_id = None
        self.points = dict() 
        self.prefix = prefix       

    def set_service(self, param_service):
        self.service_id = param_service.service_id
        self.service = param_service
        self.tags = param_service.tags

    def get_key(self):
        if self.prefix:
            return "{}::{}::{}".format(self.prefix, self.service.name, self.name)
        else:
            return "{}::{}".format(self.service.name, self.name)

    def __str__(self):
        key = self.get_key()
        return f"{self.service_id} | {self.method_id} | {key}"

class ServiceMethodEntityEncoder(JSONEncoder):
        def default(self, method: ServiceMethodEntity):
            return { 
                "method_id": method.method_id,
                "name":  method.name,
                "tags": method.tags,
                "service_id": method.service_id,
                "service": method.service.name,
                "prefix" : method.prefix     
            }