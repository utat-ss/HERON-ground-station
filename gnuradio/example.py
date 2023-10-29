from esttc_interface import esttc_rx, esttc_tx

if __name__ == '__main__':

    try:
        while True:
            esttc_tx([4,3,2,1,5])
            print(esttc_rx())
    except KeyboardInterrupt:
        print("\nExit\n")
