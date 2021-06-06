from app.Components.MetadataComponent import MetadataComponent
from app.Gateways.ConfigurationGateway import ConfigurationGateway
from app.Components.ProblemCollectComponent import ProblemCollectComponent
from app.Gateways.CSVGateway import CSVGateway
from app.Components.CollectComponent import CollectComponent
from app.Gateways.DynatraceGateway import DynatraceGateway
from datetime import datetime
import os
import logging
import urllib3
from threading import Thread, Lock


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger()    

configuration = ConfigurationGateway(use_dev=False)

dynatrace_gateway = DynatraceGateway(    
    configuration.app__dyn_host,
    configuration.app__dyn_token,
    configuration.app__dyn_tag     
)
  
file_gateway = CSVGateway(    
    configuration.app__dir_output,
    configuration.app__dyn_tag     
)

collect_component = CollectComponent(    
    file_gateway,
    dynatrace_gateway,
    configuration.app__start_on,
    configuration.app__dyn_entity,
    configuration.app__dyn_tag,
    configuration.app__dyn_prefix
)

problem_collect= ProblemCollectComponent(
    file_gateway,
    dynatrace_gateway,
    configuration.app__start_on,
    configuration.app__dyn_entity,
    configuration.app__dyn_tag,
    configuration.app__dyn_prefix
)

metadata_collect = MetadataComponent(dynatrace_gateway, configuration.app__dyn_prefix, 
    configuration.app__start_on, configuration.app__dyn_entity, configuration.app__dyn_tag, file_gateway)


def sync_job():    
    if configuration.app__enable_dyn_metric:
        try:
            collect_component.collect()            
        except Exception as e:
            logger.exception(e)
    else:
        logger.warn('dyn_reader_job disabled')    


def sync_problems_job():    
    if configuration.app__enable_dyn_problem:
        try:
            problem_collect.collect()            
        except Exception as e:            
            logger.exception(e)
    else:
        logger.warning('dyn_reader_job problems disabled') 


def sync_metadata_job():        
    if configuration.app__enable_dyn_metadata:
        try:            
            metadata_collect.collect()            
        except Exception as e:            
            logger.exception(e)
    else:
        logger.warning('read metadata disabled')    
  

if __name__ == "__main__":     
    for k in os.environ.keys():        
        if 'app__' in k:
            value = os.environ[k]
            logger.warning(f"\n ** app env  {k} : {value}")
    
    sync_metadata_job()
    for i in range(24*3):
        sync_job()
    for i in range(24*3):        
        sync_problems_job()

    
    
            
    