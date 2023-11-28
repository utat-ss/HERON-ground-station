from esttc_interface import esttc_rx, esttc_tx
import time
import zmq
import asyncio

if __name__ == '__main__':
    asyncio.run(tx_indefinitely())
    try:
        while True:
            print(esttc_rx())
    except KeyboardInterrupt:
        print("\nExit\n")

async def tx_indefinitely():
    try:
        while True:
            esttc_tx("ES+R2200\r")
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
