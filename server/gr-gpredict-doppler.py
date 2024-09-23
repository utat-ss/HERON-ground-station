import socket

HOST = 'localhost'        # Symbolic name meaning all available interfaces
PORT = 52002              # Arbitrary non-privileged port

def main():

    curr_freq = 0
    curr_tx_freq = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024).decode('ASCII').rstrip('\n')
                    if data == 'q':
                        break
                    elif data.startswith('F'):
                        curr_freq = int(data[1:])
                        print(f"curr_freq: {curr_freq}")
                        conn.sendall("RPRT 0\n".encode("UTF-8"))
                    elif data.startswith('I'):
                        curr_tx_freq = int(data[1:])
                        print(f"curr_tx_freq: {curr_tx_freq}")
                        conn.sendall("RPRT 0\n".encode("UTF-8"))
                    elif data.startswith('S') or data.startswith('AOS') or data.startswith('LOS'):
                        print(data)
                        conn.sendall("RPRT 0\n".encode("UTF-8"))
                    elif data.startswith('f'):
                        conn.sendall(f"f: {curr_freq}\n".encode("UTF-8"))
                    elif data.startswith('i'):
                        conn.sendall(f"f: {curr_tx_freq}\n".encode("UTF-8"))
                    else:
                        print(f"unkown: {data}")

                    
        except KeyboardInterrupt:
            pass

if __name__=='__main__':
    main()