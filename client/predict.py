import subprocess
import time
import re
import socket

line_pattern = re.compile(r"(\d*),.*,(-?\d*\.?\d*)")

def main():

    times = []
    shifts = []
    output = subprocess\
        .check_output(["predict", "-t", "/tmp/25544.tle", "-dp", "ISS (ZARYA)"])\
        .decode()\
        .splitlines()
    
    for line in output:
        m = line_pattern.match(line)
        times.append(int(m.group(1)))
        shifts.append(float(m.group(2)))
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect(("10.0.7.91", 52002))
            freq = 437800000
            i = 0
            curr = int(time.time())
            while curr > times[i]:
                i += 1
            while i < len(times):
                curr = int(time.time())
                time.sleep(times[i]-curr)
                time.sleep(1)
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