import subprocess
import time
import re
import socket
import requests
import tempfile

server_addr = ("10.0.7.91", 52002)
norad = 25544
freq = 437800000

def main():

    times = []
    shifts = []

    resp = requests.get(
        "https://celestrak.org/NORAD/elements/gp.php",
        params={"CATNR":str(norad)},
        timeout=5
    ).text

    tle_file = f"{tempfile.gettempdir()}/predict.tle"
    name = resp.splitlines()[0].strip()

    with open(tle_file, "w") as f:
        f.write(resp)

    output = subprocess\
        .check_output(["predict", "-t", tle_file, "-dp", name])\
        .decode()\
        .splitlines()

    line_pattern = re.compile(r"(\d*),.*,(-?\d*\.?\d*)")
    
    for line in output:
        m = line_pattern.match(line)
        times.append(int(m.group(1)))
        shifts.append(float(m.group(2)) * freq/(100e6))
    
    print("Doppler Points:")
    for i in range(len(times)):
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times[i]))
        print(f"    {formatted_time}: {shifts[i]}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect(server_addr)
            i = 0
            curr = int(time.time())
            while curr > times[i]:
                i += 1
            while i < len(times):
                curr = int(time.time())
                time.sleep(times[i]-curr)
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times[i])))
                client.sendall(f"F  {int(freq+shifts[i])}\n".encode("ASCII"))
                if(client.recv(1024).decode('UTF-8').strip() != "RPRT 0"):
                    print("bad response")
                    break
                client.sendall("f\n".encode("ASCII"))
                print(client.recv(1024).decode('UTF-8').strip())
                client.sendall(f"I  {int(freq-shifts[i])}\n".encode("ASCII"))
                if(client.recv(1024).decode('UTF-8').strip() != "RPRT 0"):
                    print("bad response")
                    break
                client.sendall("i\n".encode("ASCII"))
                print(client.recv(1024).decode('UTF-8').strip())
                i+=1
        except KeyboardInterrupt:
            pass
        
        client.sendall('q\n'.encode("ASCII"))

if __name__ == "__main__":
    main()