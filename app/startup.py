from app.Components.MySqlSyncComponent import MySqlSyncComponent
from app.Gateways.MySqlGateway import MySqlGateway
from app.Gateways.CSVGateway import CSVGateway
from app.Components.CollectComponent import CollectComponent
from app.Gateways.DynatraceGateway import DynatraceGateway
from datetime import datetime
import os
from flask import Flask
from flask_apscheduler import APScheduler
import logging
import urllib3
from threading import Thread, Lock

mutex = Lock()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.WARNING)

class Config(object):
    SCHEDULER_API_ENABLED = True

logger = logging.getLogger()    

app = Flask(__name__)

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

dynatrace_gateway = DynatraceGateway(    
    os.environ.get('app__dyn_host'),
    os.environ.get('app__dyn_token'),
    os.environ.get('app__dyn_tag')    
)
  
file_gateway = CSVGateway(
    os.environ.get('app__file_target')  
)


collect_component = CollectComponent(    
    file_gateway,
    dynatrace_gateway,
    os.environ.get('app__start_on', '2021-01-01 00:00:00'),
    os.environ.get('app__dyn_entity'),
    os.environ.get('app__dyn_tag'),
    os.environ.get('app__dyn_prefix')
)

@scheduler.task('interval', id='sync_job', seconds=20, misfire_grace_time=60)
def sync_job():
    logger.warning('sync_job at {}'.format(datetime.now()))        
    if os.environ.get('app__enable_dyn', "True") == "True":
        try:
            collect_component.collect()
            logger.warning('collect completed')
        except Exception as e:
            logger.error(e)
    else:
        logger.warning('dyn_reader_job disabled')    
   

if __name__ == "__main__":     
    for k in os.environ.keys():        
        if 'app__' in k:
            value = os.environ[k]
            logger.warning(f"\n ** app env  {k} : {value}")
            
    app.run()