# Ground Station Software Suite

## Components
* rx/
* tx/
* packet_creation/
* Test suites

## Test suites
Here's how running a test with the RX and TX system should work:

* First, fix the RX and TX systems to use your local filepaths
  * In `rx_quaddemod.grc`, edit the `path` variable block (and only the `path` variable, as the others will update automatically from that) to reflect your local instance of this repository
  * In `tx/gfsk_tx_for_test_20190817.py`, edit line 143 to reflect your local instance of this repository. The filename should still be `cmdout.bin`. For example, you could be changing it to something like `/home/myusername/Documents/UTAT/Comms/ground-station/cmdout.bin`
* Connect the transceiver and the HackRFs as follows:
  * Take the two long coax SMA cables from the wall in the lab
  * From the SMA box in the back room of the lab, take out the attenuator bag, and dig around to the clear plastic box at the bottom. Open that and take out the splitter (3-pronged SMA connected)
  * Connect the two 20 dB attenuators (the ones with the white caps) to the SMA end of the MMCX-SMA cable found in the EnduroSat box
  * Connect the RF splitter to the end of those attenuators
  * Connect the two SMA cables out of each end of the RF splitter, one into each HackRF
  * Plug the MMCX end of the MMCX-SMA connector into the transceiver
* On a Linux (Ubuntu) computer, ensure you have GNURadio installed with gr-osmosdr and gr-utat installed
* Plug BOTH HackRFs into that computer
  * Ensure both are connected by running `hackrf_info` on the command line and inspecting the response
* On that computer, open `/rx/rx_quaddemod.grc` in gnuradio-companion
* Modify the "osmocom Source" block in that GRC flowgraph to include `hackrf=1` in the "Device Arguments" parameter
* Make sure the transceiver is plugged into OBC or a laptop and receiving power
* When you're ready to do the test, go ahead and start the RX flowgraph
* Then, from the command line, run `python3 tx_test_suite_20190817.py`
* Interact with the program as instructed
* The RX flowgraph probably won't give you real time results. That's fine, just make sure to **save** and to **send** the output files (particularly, `quaddemodsignal` and `raw_recording`).
  * These files can become _very_ large if you let the flowgraph run for a long time. You could consider decimating the signal (using the `Rational Resampler` block: put 4.0032e6 in the Decimation and your desired new sample rate in the Interpolation parameters) before it goes into any of these outputs. 
  * If you choose to do that, please note that down when/if you send the files anywhere, as it informs how they're handled
  * You could also consider disabling the `quaddemodsignal_shifted` output, as that is mostly for characterization/calibration, or the `raw_recording` output, as that's mostly for me angsting about why the signals are so shitty-looking
 
## Rest to come


# OLD README -- will be scraped through and kept/scrapped later

## A note on what this repository is for
This repository should include all files that deal with the development of actual ground station functionality. This repository is *not* a catch-all for Comms or GNURadio-related files. Files like analyze_recordings.grc and the Jupyter Notebook files from the `gnuradio` repository do not belong in this repository, as they are analysis and exploratory work to help us figure out the functionality of the transceiver, rather than being programs on which the ground station will run.

When in doubt, hit me up on Slack @Gabe.

## Overview of important files
### crc16.c
* A C-language tool, to be replaced with a Python implementation, from http://srecord.sourceforge.net/crc16-ccitt.html
* If modifying this to get your checksum, please first COPY THIS FILE so the original form stays intact
* The EnduroSat transceiver appends 0x1A7D to a 1-byte "!" message. As indicated from the output of this file (just below), this is the **Bad_CRC** calculated from the **size byte concatenated with the message**
```
good_CRC = F8DF,  Bad_CRC = D5B3,  Length = 1,  Text = !
good_CRC = F926,  Bad_CRC = 2921,  Length = 8,  Text = UUUUU~!
good_CRC = D577,  Bad_CRC = 08E7,  Length = 3,  Text = ~!
good_CRC = 83B2,  Bad_CRC = 1A7D,  Length = 2,  Text = !
```
* Usage:
```
cp crc16.c localcrc16.c     # Please use this name, as it is included in the .gitignore
# Make any edits you need to main() in localcrc.16 now
gcc localcrc16.c -o crc
./crc
```

### make_message.py
* A python module to aid in the creation of messages
* Can be run explicitly, e.g. `python make_message.py`, for a usable interface
* Can also be included in a Python shell, e.g. by calling `import make_message as m`. You might want to then call `help(m)`. If you don't like the format of that help command, you can do `print(m.__doc__)` and then `print(m.<function_name>.__doc__)`, where `<function_name>` is as outputted from the first `print`
* Try not to flood the repo with too many messages... just delete/move yours if you can.

### tx.grc
* A GNURadio Companion flowgraph used for transmission of messages
* Make sure to update the file name in the "File Source" block to match your local path
* I will test out calling the python file this generates explicitly such that we don't always have to go through GNURadio
