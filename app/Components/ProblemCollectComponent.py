from app.core.DatetimeUtils import DatetimeUtils
from app.Gateways.CSVGateway import CSVGateway
from app.core.Factories.ServiceMethodFactory import ServiceMethodFactory
from app.core.Factories.ServiceFactory import ServiceFactory
from app.Gateways.DynatraceGateway import DynatraceGateway
from datetime import datetime, timedelta
import logging


class ProblemCollectComponent:

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
        self.logger = logging.getLogger(__class__.__name__)

    def collect(self): 
        current = datetime.now()
        pivot = self.csv_gateway.get_problem_anchor()        
        if self.start_on < pivot:
            self.start_on = pivot        
        limit = datetime(current.year, current.month, current.day)
        if self.start_on < limit:        
            next_date = self.start_on + timedelta(hours=23, minutes=59, seconds=59)        
            self.logger.warning("problem sync {} sli between {} - {}".format(self.entity_tag, 
                self.start_on, next_date))            
            self.__load_dynatrace_data(self.start_on, next_date)
            self.start_on = next_date + timedelta(seconds=1)       
        else:
            self.logger.warning("limit {}".format(limit))
    
    def __load_dynatrace_data(self, start, end: datetime):
        problems = self.dynatrace_gateway.get_problems(start, end)
        items = sorted(problems["result"]["problems"], 
                       key=lambda x: DatetimeUtils.convert_from_timestamp(int( x['endTime']) ))
        for problem in items:
            key = "{}".format(problem['startTime'])             
            self.logger.info("problem {}".format(problem['displayName']))
            problem['startTime'] = DatetimeUtils.convert_from_timestamp(int(problem['startTime'])).isoformat()
            problem['endTime'] = DatetimeUtils.convert_from_timestamp(int(problem['endTime'])).isoformat()
            self.csv_gateway.create_problem_entry(key, problem)
            

