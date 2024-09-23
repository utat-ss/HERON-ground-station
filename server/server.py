import socket
import sys
sys.path.append('transceivers')
import hackrf_trx
import signal
import sys
import importlib



def main():

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(('0.0.0.0', 50600))
    flow = hackrf_trx.hackrf_trx()

    run = True
    
    def sig_handler(sig=None, frame=None):
        nonlocal serv
        nonlocal flow
        nonlocal run
        run = False
        flow.stop()
        serv.shutdown(socket.SHUT_RDWR)
        serv.close()
        flow.wait()
        print('bye')

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    while run:
        try:
            serv.listen(1)
            client, client_addr = serv.accept()
            flow.start()
            client.recv(1024)
        except (OSError, socket.error) as e:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            print('client bye')
        flow.stop()

if __name__ == '__main__':
    main()