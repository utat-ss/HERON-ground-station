import tempfile
import re
import os
import subprocess

class PredictWrapper():

    def __init__(self, callsign: str, latitude: int, longitude: int):
        self.qth_file = tempfile.NamedTemporaryFile(
            "w+",
            suffix=".db",
            delete=False)
        self._callsign = callsign
        self._latitude = latitude
        self._longitude = longitude
        self.qth_file.close()
        self.update_qth_file()
    
    def __del__(self):
        try: os.remove(self.qth_file.name)
        except: pass
    
    def update_callsign(self, new_callsign: str):
        self._callsign = new_callsign
        self.update_qth_file()

    def update_latitude(self, new_latitude: int):
        self._latitude = new_latitude
        self.update_qth_file()
    
    def update_longitude(self, new_longitude: int):
        self._longitude = new_longitude
        self.update_qth_file()
        
    def update_qth_file(self):
        with open(self.qth_file.name, mode='w+') as f:
            f.write(self._callsign)
            f.write("\n ")
            f.write(str(self._latitude))
            f.write("\n ")
            f.write(str(-self._longitude)) # predict uses west positive!
            f.write("\n")
    
    def get_doppler_shifts(self, tle_file: str, sat_name: str):
        output = subprocess\
            .check_output(["predict", "-q", self.qth_file.name, "-t", tle_file, "-dp", sat_name])\
            .decode()\
            .splitlines()
        line_pattern = re.compile(r"(\d*),.*,(-?\d*\.?\d*)")
        times = []
        shifts = []
        for line in output:
            m = line_pattern.match(line)
            times.append(int(m.group(1)))
            shifts.append(float(m.group(2)))
        return (times, shifts)

    def get_next_pass(self, tle_file: str, sat_name: str):
        output = subprocess\
            .check_output(["predict", "-q", self.qth_file.name, "-t", tle_file, "-p", sat_name])\
            .decode()\
            .splitlines()
        line_pattern = re.compile(r"^(\d+)\s\S+\s\S+\s\S+\s+(\d*\.?\d*)")
        times = []
        elevs = []
        for line in output:
            m = line_pattern.match(line)
            times.append(int(m.group(1)))
            elevs.append(float(m.group(2)))
        return times[0], max(elevs)