from app.core.ServiceMethodEntity import ServiceMethodEntityEncoder
from app.core.DatetimeUtils import DatetimeUtils
from datetime import datetime
from os import walk
import os
from collections import deque
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.parser import parse
from os import path
import json
import logging
import glob

class CSVGateway:

    def __init__(self, app_dir_output, app_dyn_tag):      
        self.app_dyn_tag = app_dyn_tag.replace(":", "_")          
        self.logger = logging.getLogger(__class__.__name__)
        self.current_output_dir = app_dir_output
        self.current_path = path.join(app_dir_output, f"{self.app_dyn_tag}.csv")
        if not os.path.exists(self.current_path):
            print('creating file  {} '.format(self.current_path))
            try:
                with open(self.current_path, 'w'): pass
            except:                
                pass

        if not os.path.isdir(path.join(app_dir_output, "problems")):
            os.makedirs(path.join(app_dir_output, "problems"))

        self.current_problem_dir = path.join(app_dir_output, f"problems/{app_dyn_tag}")

        if not os.path.isdir(self.current_problem_dir):
            os.makedirs(self.current_problem_dir)

        if not os.path.isdir(path.join(app_dir_output, "dynmetadata")):
            os.makedirs(path.join(app_dir_output, "dynmetadata"))

        self.current_metadata_file = path.join(app_dir_output, f"dynmetadata/{app_dyn_tag}.json")
        

    def post_metadata(self, model):        
        with open(self.current_metadata_file, 'w') as f:
            f.write(json.dumps(model, indent=4, cls=ServiceMethodEntityEncoder))
            
    def create_problem_entry(self, key, model):
        target = path.join(self.current_problem_dir, f"{key}.json")
        if not os.path.exists(target):
            with open(target, 'w') as f:
                f.write(json.dumps(model, indent=4))
        else:
            self.logger.info("file {} already exists".format(target))

    def get_problem_anchor(self):
        
        if len(os.listdir(self.current_problem_dir)) > 0:            
            _, _, files = next(walk(self.current_problem_dir))
            last_file = max(files)
            last_file = last_file.replace(".json", "")
            d = DatetimeUtils.convert_from_timestamp(int(last_file))
            return datetime(d.year, d.month, d.day)  
        else:    
            d = datetime.now()
            return datetime(d.year, 1, 1, 0, 0, 0)


    def create_source(self, source, start, end, total, availability_good, experience_good, latency):
        with open(self.current_path, 'a') as f:
            f.write("{};{};{};{};{};{};{}\n".format(source, start, end,
                                                    total,
                                                    availability_good,
                                                    experience_good,
                                                    latency))

    def get_anchor(self):
        if Path(self.current_path).stat().st_size:
            with open(self.current_path, 'r') as f:
                q = deque(f, 1)
                str_date = q.pop().split(';')[2]
                target = parse(str_date) + timedelta(seconds=1)
                return target
        else:
            d = datetime.now()
            return datetime(d.year, 1, 1, 0, 0, 0)

    
    def get_data_from(self, anchor: datetime):
        result = list()
        if Path(self.current_path).stat().st_size:
            with open(self.current_path, 'r') as f:
                current_date = None
                while True:
                    line = f.readline()                                    
                    if not line:
                        break
                    str_date = line.split(';')[2]
                    target = parse(str_date) 
                    if current_date is None and target > anchor:
                        current_date = target
                    
                    if current_date:
                        if current_date == target:
                            result.append(line)
                        elif target > current_date:
                            break                
        return result     

        
