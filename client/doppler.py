from xmlrpc.client import ServerProxy

def main():
    dpler = ServerProxy("http://10.0.7.91:50600")
    dpler.load_norad(25544)
    dpler.set_freq(437_800_000)
    dpler.enable_correction()
    input('Press Enter to quit')
    dpler.disable_correction()

if __name__ == "__main__":
    main()