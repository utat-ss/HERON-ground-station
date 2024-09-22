import subprocess
import time
import re
import socket

line_pattern = re.compile(r'(\d*),.*,(-?\d*\.?\d*)')

def main():

    times = []
    shifts = []
    output = subprocess\
        .check_output(['predict', '-t', '/home/swarnava/58287.txt', '-dp', 'PICO-01B009'])\
        .decode('utf-8')\
        .splitlines()
    
    for line in output:
        m = line_pattern.match(line)
        times.append(int(m.group(1)))
        shifts.append(float(m.group(2)))
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect(('10.0.7.91', 52002))
            freq = 435000000
            curr = int(time.time())
            i = 0
            while curr > times[i]:
                i += 1
            while i < len(times):
                time.sleep(times[i]-curr)
                client.sendall(f'F{freq+shifts[i]}'.encode())
                client.sendall(f'I{freq-shifts[i]}'.encode())
                i+=1
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()