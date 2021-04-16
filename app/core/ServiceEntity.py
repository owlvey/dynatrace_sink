from app.core.ServiceMethodEntity import ServiceMethodEntity


class ServiceEntity:

    def __init__(self, service_id, name):        

        if not service_id:            
            raise ValueError('service id required')
        if not name:
            raise ValueError('name required')

        self.service_id = service_id
        self.name = name
        self.tags = list()
        self.methods = dict()
        self.methods_days = dict()

        

    def get_method_name(self, method_id):
        return self.methods[method_id]

    def load_method(self, method: ServiceMethodEntity):
        if method.method_id not in self.methods:
            self.methods_days[method.method_id] = dict()
            self.methods[method.method_id] = method.name

        tmp = self.methods_days[method.method_id]

        for key, value in method.points.items():
            if key not in tmp:
                tmp[key] = [0, 0, 0, 0]
        return tmp

    def load_methods_total_information(self, total_method: ServiceMethodEntity):
        tmp = self.load_method(total_method)
        for key, value in total_method.points.items():
            tmp[key] = [value, value, value, 0]

    def load_methods_fail_information(self, fail_method: ServiceMethodEntity):
        tmp = self.methods_days[fail_method.method_id]
        for key, value in fail_method.points.items():
            result = tmp[key][0] - value
            tmp[key][1] = 0 if result < 0 else result

    def load_methods_experience_information(self, fail_method: ServiceMethodEntity):
        tmp = self.methods_days[fail_method.method_id]
        for key, value in fail_method.points.items():
            result = tmp[key][0] - value
            tmp[key][2] = 0 if result < 0 else result

    def load_methods_latency_information(self, latency_method: ServiceMethodEntity):
        tmp = self.methods_days[latency_method.method_id]
        for key, value in latency_method.points.items():
            tmp[key][3] = value / 1000  # ticks to miliseconds

    def __str__(self):
        return "{} {}".format(self.service_id, self.name)



