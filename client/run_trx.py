
import stations

if __name__ == '__main__':

    # (client, channel, flow, digi, rot) = stations.setup_herongs(rot_config="lab")
    (client, channel, flow, digi, rot) = stations.setup_pluto(rx_config="partial")
    flow.set_output("/tmp/test.fc32")

    input("Press Enter to quit...\n")
    print("Exitting...")
    
