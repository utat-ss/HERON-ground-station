"""
propagate.py

Using the SatNOGS API to find feasible pass windows and estimate when they will occur.

Author(s): Adyn Miles
"""
from datetime import datetime
import requests
from pprint import pprint
'''

TODO :
- [Done] Access the SatNOGS network client API
- [Done] Have it return the valid pass times for a given satellite ID.

'''

class Propagator():
    def __init__(self, satellite_id):
        self.satellite_info = requests.get('https://network.satnogs.org/api/observations/%s' % satellite_id)
        self.satellite_info = self.satellite_info.json()
    def get_pass_times(self):
        start_time = self.satellite_info["start"]
        start_time = start_time.strip("Z")
        start_time = start_time.replace("T", " ")
        end_time = self.satellite_info["end"]
        end_time = end_time.strip("Z")
        end_time = end_time.replace("T", " ")
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        return [start_time, end_time]
