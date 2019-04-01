# Ground Station Software Suite

## crc16.c
* A C-language tool, to be replaced with a Python implementation, from http://srecord.sourceforge.net/crc16-ccitt.html
* If modifying this to get your checksum, please first COPY THIS FILE so the original form stays intact
* The EnduroSat transceiver appends 0x1A7D to a 1-byte "!" message. As indicated from the output of the original form of this `crc16.c` file, this is the **BAD CRC** output of the **size byte concatenated with the message**
* Usage:
```
cp crc16.c localcrc16.c` # Please use this name, as it is included in the .gitignore
gcc crc16.c -o crc`
./crc
```

## make_message.py
* A python module to aid in the creation of messages
* Can be run explicitly, e.g. `python make_message.py`, for a usable interface
* Can also be included in a Python shell, e.g. by calling `import make_message as m`. You might want to then call `help(m)`. If you don't like that `help(m)` opens in a `more` menu, you can `print(m.__doc__)` and then `print(m.<function_name>.__doc__)`, where <function_name> are those listed in the original print
* Try not to flood the repo with too many messages... just delete/move yours if you can.

## tx.grc
* A GNURadio Companion flowgraph used for transmission of messages
* Make sure to update the file name in the "File Source" block to match your local path
* I will test out calling the python file this generates explicitly such that we don't always have to go through GNURadio
