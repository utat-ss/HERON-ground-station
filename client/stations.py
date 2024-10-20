import rpyc
from xmlrpc.client import ServerProxy
import subprocess
import time
from esttc_interface import ESTTCWrapper

def setup_herongs(rot_config=None, tx_config=None, rx_config=None):

    ip = "10.0.7.91"

    print("[stations] starting HERON GS transceiver")

    trx = subprocess.Popen(
        [
            "ssh", f"heron@{ip}", "-t", """
            cd HERON-ground-station/server/transceivers;
            ./utils/enable_hackrf_clocks.sh;
            grcc hackrf_trx.grc;
            python3 hackrf_trx.py"""
        ],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print("[stations] setting up HERON GS rotator")

    rot = rpyc.connect(ip, 18866).root.K3NG
    if isinstance(rot_config, str) and rot_config == "lab":
        for i in range(5):
            try:
                rot.set_azimuth(38)
                rot.set_elevation(5)
                break
            except: pass
    elif isinstance(rot_config, int) and rot_config > 0:
        for i in range(5):
            try:
                rot.load_and_track(rot_config)
                rot.enable_tracking()
                break;
            except: pass
    else:
        pass

    print("[stations] setting up HERON GS transceiver")

    for _ in range(10):
        s = trx.stdout.read1().decode()
        if "Press Enter to quit:" in s:
            break

    flow = ServerProxy(f"http://{ip}:8080")
    if isinstance(tx_config, int):
        flow.set_pa(True)
        flow.set_tx_pwr(tx_config)
    else:
        flow.set_pa(False)
    flow.set_lna(True)
    flow.set_rx_amp(True)
    flow.set_rx_vga_gain(62)
    flow.set_rx_if_gain(40)
    digi = ESTTCWrapper(f"tcp://{ip}:50491", f"tcp://{ip}:50492")

    print("[stations] done setting up HERON GS")

    return (trx, flow, digi, rot)

def setup_pluto(rx_config=None):

    ip = "10.0.1.165"

    print("[stations] starting PLUTO transceiver")

    trx = subprocess.Popen(
        [
            "ssh", f"heron@{ip}", "-t", """
            cd HERON-ground-station/server/transceivers;
            grcc pluto_trx.grc;
            python3 pluto_trx.py"""
        ],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print("[stations] setting up PLUTO transceiver")

    for _ in range(10):
        s = trx.stdout.read1().decode()
        if "Press Enter to quit:" in s:
            break

    flow = ServerProxy(f"http://{ip}:8080")
    flow.set_tx_gain(89.75)
    if isinstance(rx_config, str):
        if rx_config == "partial":
            flow.set_rx_gain(4)
        elif rx_config == "full":
            flow.set_rx_gain(71)
    digi = ESTTCWrapper(f"tcp://{ip}:50491", f"tcp://{ip}:50492")

    print("[stations] done setting up PLUTO")
    
    return (trx, flow, digi, None)

