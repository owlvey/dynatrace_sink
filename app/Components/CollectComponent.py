from app.Gateways.CSVGateway import CSVGateway
from app.core.Factories.ServiceMethodFactory import ServiceMethodFactory
from app.core.Factories.ServiceFactory import ServiceFactory
from app.Gateways.DynatraceGateway import DynatraceGateway
from datetime import datetime, timedelta
import logging


class CollectComponent:

    def __init__(self,         
        file_gateway: CSVGateway,
        dynatrace_gateway: DynatraceGateway, 
        start_on, entity_name, entity_tag, entity_prefix) -> None:
        self.start_on = datetime.strptime(start_on, '%Y-%m-%d %H:%M:%S')
        self.csv_gateway = file_gateway
        self.dynatrace_gateway = dynatrace_gateway
        self.entity_name = entity_name
        self.entity_tag = entity_tag
        self.prefix = entity_prefix
        self.logger = logging.getLogger()


    def collect(self):
        current = datetime.now()
        pivot_sli = self.csv_gateway.get_anchor()

        if self.start_on < pivot_sli:
            self.start_on = pivot_sli
        
        limit = datetime(current.year, current.month, current.day) + timedelta(hours=-3)

        if self.start_on < limit:        
            next_date = self.start_on + timedelta(minutes=59, seconds=59)        
            self.logger.warning("\n sync {} sli between {} - {}".format(self.entity_tag, self.start_on, next_date))            
            self.__load_dynatrace_data(self.start_on, next_date)
            self.start_on = next_date + timedelta(seconds=1)                                

    def __internal_load_dynatrace_data(self, start, end):
        services = self.dynatrace_gateway.get_services()
        service_methods = self.dynatrace_gateway.get_service_methods_totals(start, end)
        fail_service_methods = self.dynatrace_gateway.get_fail_service_methods_totals(start, end)
        service_entities = ServiceFactory.parse(services, self.entity_name, self.entity_tag)

        methods_entities = ServiceMethodFactory.parse(service_entities, service_methods)
        fail_method_entities = ServiceMethodFactory.parse(service_entities, fail_service_methods)

        bad_service_methods = self.dynatrace_gateway.get_fail_service_methods_400(start, end)
        bad_method_entities = ServiceMethodFactory.parse(service_entities, bad_service_methods)

        latency_methods = self.dynatrace_gateway.get_service_methods_latency(start, end)
        latency_method_entities = ServiceMethodFactory.parse(service_entities, latency_methods)

        return service_entities, methods_entities, fail_method_entities, bad_method_entities, latency_method_entities

    def __load_method(self, service_entities, method, load_total):
        if method.service_id in service_entities:
            item = service_entities[method.service_id]
            if load_total == 0:
                item.load_methods_total_information(method)
            elif load_total == 1:
                item.load_methods_fail_information(method)
            elif load_total == 2:
                item.load_methods_experience_information(method)
            else:
                item.load_methods_latency_information(method)
        else:
            raise ValueError("service not found " + str(method))

    def __load_dynatrace_data(self, start, end):
        service_entities, methods_entities, fail_method_entities, bad_method_entities, latency_method_entities = self.__internal_load_dynatrace_data(start, end)

        for method in methods_entities:
            self.__load_method(service_entities, method, 0)

        for method in fail_method_entities:
            self.__load_method(service_entities, method, 1)

        for method in bad_method_entities:
            self.__load_method(service_entities, method, 2)

        for method in latency_method_entities:
            self.__load_method(service_entities, method, 3)

        for service_id, item in service_entities.items():

            for key, value in item.methods_days.items():

                target_method = item.get_method_name(key)

                if self.prefix:
                    source = "{}::{}::{}".format(self.prefix, item.name, target_method)
                else:
                    source = "{}::{}".format(item.name, target_method)

                for date, vector in value.items():

                    total = int(vector[0])
                    availability = int(vector[1])
                    experience = int(vector[2])
                    latency = vector[3]
                    if availability < 0:
                        self.logger.warning("availability error , good is less than zero for {} ".format(source))
                        availability = 0
                    if experience < 0:
                        self.logger.warning("experience error , good is less than zero for {} ".format(source))
                        experience = 0

                    if total < 0:
                        self.logger.warning("total , total is less than zero for {} ".format(source))
                        total = 0

                    if total < availability or total < experience or (total == 0 and latency > 0):
                        self.logger.warning("weird value total:{} ava:{} exp:{} latency:{} source:{} method_id:{}".format(total, availability, experience, latency, source, key))
                    else:
                        self.csv_gateway.create_source(source, start, end, total, availability, experience, latency)
                        


