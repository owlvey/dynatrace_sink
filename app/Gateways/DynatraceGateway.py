import requests
from datetime import datetime
from app.core.DatetimeUtils import DatetimeUtils


PROXY_DIR = {
    "http": "",
    "https": ""
}

class DynatraceGateway:

    __cache_get_services = None

    def __init__(self, dynatrace_host, dynatrace_token, dynatrace_tag_service):        
        self.token = "Api-Token {}".format(dynatrace_token)
        self.host = dynatrace_host
        self.service_tag = dynatrace_tag_service        

    def get_services(self):
        if not DynatraceGateway.__cache_get_services:            
            response = requests.get(self.host + "entity/services?includeDetails=true&tag={}&includeParentIds=true".format(self.service_tag),
                                    headers={"Authorization": self.token,
                                            "accept": "application/json"}, 
                                            verify=False, proxies = PROXY_DIR)

            if response.status_code != 200:
                raise ValueError(response.status_code)
            
            DynatraceGateway.__cache_get_services = response.json()

        return DynatraceGateway.__cache_get_services

    def get_fail_service_methods_totals(self, start, end):
        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)

        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.errorcounthttp5xx?includeData=true&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&tag={}&includeParentIds=true".format(
            start_stamp, end_stamp, self.service_tag)
        response = requests.get(target_url,
                                headers={"Authorization": self.token, "accept": "application/json"}, 
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_fail_service_method_totals(self, start, end, method_id):
        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)

        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.errorcounthttp5xx?includeData=true&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&entity={}&tag={}&includeParentIds=true".format(
            start_stamp, end_stamp, method_id, self.service_tag)
        response = requests.get(target_url,
                                headers={"Authorization": self.token, "accept": "application/json"}, 
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_fail_service_methods_400(self, start, end):
        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)
        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.errorcounthttp4xx?includeData=true&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&tag={}&includeParentIds=true".format(
            start_stamp, end_stamp, self.service_tag)

        response = requests.get(target_url,
                                headers={"Authorization": self.token, "accept": "application/json"}, 
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_fail_service_method_400(self, start, end, method_id):
        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)
        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.errorcounthttp4xx?includeData=true&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&entity={}&tag={}&includeParentIds=true".format(
            start_stamp, end_stamp, method_id, self.service_tag)

        response = requests.get(target_url,
                                headers={"Authorization": self.token, "accept": "application/json"}, 
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_service_methods_totals(self, start, end):
        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)

        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.requests?includeData=true&aggregationType=COUNT&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&tag={}&includeParentIds=true".format(
            start_stamp, end_stamp, self.service_tag)
        response = requests.get(target_url, headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_service_method_totals(self, start, end, method_id):

        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)
        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.requests?includeData=true&aggregationType=COUNT&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&entity={}&tag={}&includeParentIds=true".format(
            start_stamp, end_stamp, method_id, self.service_tag)
        response = requests.get(target_url, headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_service_methods_latency(self, start, end):

        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)
        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.responsetime?includeData=true&aggregationType=PERCENTILE&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&tag={}&percentile=95&includeParentIds=true".format(
            start_stamp, end_stamp, self.service_tag)
        response = requests.get(target_url, headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_service_method_latency(self, start, end, entity, percentile):

        if percentile < 1:
            percentile = percentile * 100

        percentile = int(percentile)

        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)

        target_url = self.host + "timeseries/com.dynatrace.builtin:servicemethod.responsetime?includeData=true&aggregationType=PERCENTILE&startTimestamp={}&endTimestamp={}&queryMode=TOTAL&entity={}&tag={}&percentile={}&includeParentIds=true".format(
            start_stamp, end_stamp, entity, percentile, self.service_tag)
        response = requests.get(target_url, headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_web_key_error_percentaje(self, start, end):

        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)

        target_url = self.host + "timeseries/com.dynatrace.builtin%3Aappmethod.errorpercentage?includeData=true&aggregationType=COUNT&startTimestamp={}&endTimestamp={}&queryMode=SERIES&tag={}&includeParentIds=true".format(
            start_stamp, end_stamp, self.service_tag)
        response = requests.get(target_url, headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False, proxies = PROXY_DIR)

        if response.status_code != 200:
            raise ValueError(response.status_code)

        return response.json()

    def get_problems(self, start, end):
        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)        
        target_url = self.host + "problem/feed?tag={}&status=CLOSED&startTimestamp={}&endTimestamp={}".format(
            self.service_tag, start_stamp, end_stamp)
        response = requests.get(target_url,  
                                headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False, proxies = PROXY_DIR)

        if response.status_code > 299:
            raise ValueError(response.status_code)

        return response.json()

    


