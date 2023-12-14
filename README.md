# Ground Station Software Suite

Ground station documentation describing the use of this repository as well as the [gr-utat](https://github.com/HeronMkII/gr-utat) repository.

## GNURadio Set-up
* Download and install GNURadio v3.8 through whatever means you want. Technically PyBOMBS is preferred, but any method should function
* Clone the gr-utat repository as well as gr-osmosdr (https://github.com/osmocom/gr-osmosdr) and gr-gpredict (https://github.com/ghostop14/gr-gpredict-doppler)
* For each of those repos, run the following commands:

```cd <local repo>/
mkdir build
cd build/
cmake ../
make
sudo make install
sudo ldconfig
```

## gr-utat/

* A GNURadio out-of-tree module written for HERON Ground RX
* You won’t need to look in most of the folders. The most important one is lib/
* In lib/, you will find heron_rx_bb_impl.cc (Heron RX is the name of the block, BB is for byte-to-byte, IMPL is for implementation). The gist of the block’s functionality is it consumes a block of data, combing through it for a packet. Upon finding each section of the packet, storing its data, and confirm the checksum is correct, it will print out the packet data and exit the process early, consuming only the bytes up to the end of the packet 
 *	The purpose for the early exit was a simple/hacky way of making sure only packet content got forwarded out of the block, and as the consumption of the next data block will begin at the end of the previous packet, it won’t lead to dropped packets
*	Follow instructions in the GNURadio tutorial for creating a new block in this module. Push changes to gr-utat to keep it as one shared module for the different blocks

## ground-station/

### README.md
* This file

###	interface/
*	NB: I’ve copied the “Tx_for_bidirectional.py” file to the parent directory to run it as the relative path this file uses to run the tx flowgraph wasn’t working otherwise. It was a lazy solution when we were testing.
*	commands.py :: a minimally populated JSON list of the satellite commands according to SS-HERON-0008. Goal was to parametrize each command and automate message generation (the following file shows how this is used)
*	tx_for_bidirectional.py :: a CLI program for sending various ESTTC and HERON commands to the satellite
 *	Of note: this was for the manual bidirectional test, and does not actually block and wait on / confirm a response, because RX was faulty
 *	The general logic loop followed in this file is the model for implementing manual or automated TX, though. This file can be copied and modified to interface with wherever RX data is written once RX works. I had a few ideas for implementing this – if y’all are crunched, once we’re actually getting reliable RX data output from the block I can help edit this and the HERON RX block to implement a full TX/RX control loop
*	tx_test_suite.py :: an older version of tx_for_bidirectional.py

### messages/
* 	A folder of important binary message files. Mostly for hard-implementing ESTTC commands, which follow a different format than HERON commands. The other two files in here were for testing purposes

### packet_creation/
* Python code to help with the creation of HERON command packets
*	You’ll really only have to use the main() interface in this, or worry about the details of these functions, if you’re trying to create another ESTTC packet

### rx/
*	includes the RX flowgraph

### tx/
*	Includes the tx flowgraph, and a compiled copy of an old version of the tx flowgraph that I’m pretty sure can be removed. 
*	I’m pretty sure I’ve moved this to the parent directory in my local copy – will confirm

### website/
*	An old Comms member was working on implementing a web interface. The UI was implemented, but it was never connected to a backend that had it actually call the GNURadio flowgraphs
