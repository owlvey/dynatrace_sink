from typing import List
from app.core.DatetimeUtils import DatetimeUtils
from app.core.ServiceEntity import ServiceEntity
from app.core.ServiceMethodEntity import ServiceMethodEntity


class ServiceMethodFactory:

    @staticmethod
    def parse(services: dict, target, prefix):
        
        result = list()
        methods = {}
        data = target["dataResult"]
        data_entities = data["entities"]

        for k, v in data_entities.items():
            if "SERVICE_METHOD" in k:
                tmp = ServiceMethodEntity(prefix)
                tmp.name = v
                tmp.method_id = k
                methods[k] = tmp
            elif "SERVICE" in k:
                if k not in services:
                    tmp = ServiceEntity(k, v)                    
                    services[k] = tmp

        data_points = data["dataPoints"]

        for k, v in data_points.items():
            service_id, method_id = k.split(",")
            method = methods[method_id.strip()]            
            method.set_service(services[service_id])            
            
            for item in v:
                stamp_date = DatetimeUtils.convert_from_timestamp(item[0])
                if item[1]:
                    date_key = stamp_date
                    if date_key in method.points:
                        raise ValueError('duplicate entry')
                    else:
                        method.points[date_key] = item[1]

        for k, v in methods.items():
            if v.points:
                result.append(v)

        return result


