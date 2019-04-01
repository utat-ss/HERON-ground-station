# Ground Station Software Suite

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
