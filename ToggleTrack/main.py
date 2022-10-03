# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import os
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from base64 import b64encode
from pprint import pprint
from datetime import datetime

try:
    import certifi
    cafile = certifi.where()
except ImportError:
    pass

class Endpoints():
    REPORT_DETAILED = "https://api.track.toggl.com/reports/api/v2/details"


class Toogle():
    # template of headers for request
    headers = {
        "Authorization": "",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "python/urllib",
    }

    # default API user agent value
    user_agent = "sva7777"

    def setAPIKey(self, APIKey):
        '''set the API key in the request header'''
        # craft the Authorization
        authHeader = APIKey + ":" + "api_token"
        authHeader = "Basic " + b64encode(authHeader.encode()).decode('ascii').rstrip()

        # add it into the header
        self.headers['Authorization'] = authHeader

    def requestRaw(self, endpoint, parameters=None):
        if parameters is None:
            return urlopen(Request(endpoint, headers=self.headers), cafile=cafile).read()
        else:
            if 'user_agent' not in parameters:
                parameters.update({'user_agent': self.user_agent})  # add our class-level user agent in there
            # encode all of our data for a get request & modify the URL
            endpoint = endpoint + "?" + urlencode(parameters)
            # make request and read the response
            return urlopen(Request(endpoint, headers=self.headers), cafile=cafile).read()

    def request(self, endpoint, parameters=None):
        return json.loads(self.requestRaw(endpoint, parameters).decode('utf-8'))

    def getDetailedReport(self, data):
        return self.request(Endpoints.REPORT_DETAILED, parameters=data)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        pprint("не коррректные параметры скрипта. Правильные %дата(2022-09-24)% %workspace_id%  %api_key%")
    date_of_report =sys.argv[1]
    workspace_id = sys.argv[2]
    api_key = sys.argv[3]


    data = {
        # ToDo move workspace_id to OS env variable
        'workspace_id': workspace_id,
        'since': date_of_report,
        'until': date_of_report,
        'page':1,
    }

    toggle = Toogle()

    # ToDo move key to OS env variable
    toggle.setAPIKey(api_key)

    tasks = list()
    while True:

        result = toggle.getDetailedReport(data)
        # ToDo add result check



        tasks.extend(result['data'])

        # ToDo check are total_count and per_page exist
        if result['total_count'] < result['per_page'] * data['page']:
            break

        data['page'] = data['page'] + 1




    # ToDo remove this data dublication
    tasks_list = []

    for task in tasks:
        local = dict()
        local['project'] = task['project']
        local['description'] = task['description']
        local['start'] = datetime.strptime(task['start'], '%Y-%m-%dT%H:%M:%S+03:00')
        local['end'] = datetime.strptime(task['end'], '%Y-%m-%dT%H:%M:%S+03:00')

        tasks_list.append(local)

    # sort tasks_list by start time

    tasks_list = sorted(tasks_list, key=lambda x: x['start'])

    print("старт    стоп     описание (длительность чч:мм:cc)")
    for task in tasks_list:
        print("{:8} {:8} {}:{} (длительность {})".format(task['start'].strftime("%H:%M:%S") ,task['end'].strftime("%H:%M:%S") ,task['project'],task['description'] , task['end']- task['start']   ))
        print("")

