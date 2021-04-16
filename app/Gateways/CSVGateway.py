from datetime import datetime
import pathlib
import os
from collections import deque
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.parser import parse

class CSVGateway:

    def __init__(self, target_file):        
        self.current_path = target_file
        if not os.path.exists(self.current_path):
            print('creating file  {} '.format(self.current_path))
            try:
                with open(self.current_path, 'w'): pass
            except:
                pass

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

        
