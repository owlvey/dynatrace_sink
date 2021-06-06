from types import MethodDescriptorType
from app.Gateways.CSVGateway import CSVGateway
from app.core.Factories.ServiceMethodFactory import ServiceMethodFactory
from app.core.Factories.ServiceFactory import ServiceFactory
from app.Gateways.DynatraceGateway import DynatraceGateway
from datetime import datetime, timedelta


class MetadataComponent:
    def __init__(self, dynatrace_gateway: DynatraceGateway, entity_prefix, 
        start_on, entity_name, entity_tag, file_gateway: CSVGateway) -> None:
        self.prefix = entity_prefix
        self.start_on = datetime.strptime(start_on, '%Y-%m-%d %H:%M:%S')
        self.dynatrace_gateway = dynatrace_gateway
        self.cache = None
        self.csv_gateway = file_gateway
        self.entity_name =  entity_name
        self.entity_tag = entity_tag

    def seek(self):
        if not self.cache:
            services = self.dynatrace_gateway.get_services()
            service_methods = self.dynatrace_gateway.get_service_methods_totals(self.start_on, datetime.now())
            service_entities = ServiceFactory.parse(services, self.entity_name, self.entity_tag)
            methods_entities = ServiceMethodFactory.parse(service_entities, service_methods, self.prefix)
            self.cache = methods_entities
        return self.cache

    def collect(self):
        model = self.seek()
        self.csv_gateway.post_metadata(model)
