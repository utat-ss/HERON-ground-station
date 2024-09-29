from xmlrpc.client import ServerProxy
import rpyc
import ax25


def main():
    norad = 25544
    freq = 437_800_000
    ip = "10.0.7.91"

    rot = rpyc.connect(ip, 18866).root.K3NG
    rot.load_and_track(norad)
    rot.enable_tracking()
    print(rot.get_tracking_status())

    flow = ServerProxy(f"http://{ip}:8080")
    flow.set_cfo(freq + 100_000)
    flow.set_freq(freq)
    flow.set_lna(True)
    flow.set_rx_vga_gain(62)
    flow.set_rx_if_gain(40)
    flow.set_rx_amp(True)
    flow.set_pa(False)
    flow.set_mode(0)
    flow.set_squelch_threshold(-21)

    dpler = ServerProxy(f"http://{ip}:50600")
    dpler.load_norad(norad)
    dpler.set_freq(freq)
    dpler.enable_correction()


    input('Press Enter to quit')
    dpler.disable_correction()

if __name__=="__main__":
    main()