from xmlrpc.client import ServerProxy
import stations

def main():

    norad = 25544
    freq = 437_800_000

    (trx, flow, gs_digi, rot) = stations.setup_herongs(rot_config=norad)

    print(rot.get_tracking_status())

    flow.set_cfo(freq + 100_000)
    flow.set_freq(freq)
    flow.set_squelch_threshold(-21)
    flow.set_mode(0)

    dpler = ServerProxy(f"http://10.0.7.91:50600")
    dpler.load_norad(norad)
    dpler.set_freq(freq)
    dpler.enable_correction()

    input('Press Enter to quit')
    rot.disable_tracking()
    dpler.disable_correction()

if __name__=="__main__":
    main()