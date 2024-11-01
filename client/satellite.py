import tempfile
import requests
import os

class Satellite:

    norad: int
    freq: int
    mode: int
    name: str
    tle_file: tempfile._TemporaryFileWrapper

    def __init__(self, norad:int, freq:int, mode:int):
        self.norad = norad
        self.freq = freq
        self.mode = mode
        self.tle_file = tempfile.NamedTemporaryFile(
            "w+",
            suffix=".tle",
            delete=False,
            delete_on_close=False)
        self.tle_file.close()
        self.update_tle()
    
    def __del__(self):
        try: os.remove(self.tle_file.name)
        except: pass
    
    def update_tle(self):
        resp = requests.get(
            "https://celestrak.org/NORAD/elements/gp.php",
            params={"CATNR":str(self.norad)},
            timeout=5
        ).text
        if "No GP data found" in resp:
            raise LookupError("norad does not exist")
        self.name = resp.splitlines()[0].strip()
        with open(self.tle_file.name, mode='w+') as f:
            f.write(resp)