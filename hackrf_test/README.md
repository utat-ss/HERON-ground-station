# HackRF Testing Using GNURadio

The .grc files in this folder are used for testing
the HackRF's for viable transmission and reception

Due to IQ sampling issues, the rx HackRF cannot be tuned
to the same frequency that it is trying to analyze. Instead,
it should be tuned to a nearby frequency and then the specturm
should be shifted using the `frequency shift` block within
GNURadio so that the original center is now outside the band
we are trying to analyze. For example, if we want to listen to
an FM station on 98.3 MHz with a bandwidth of 200 kHz, then we might
tune the HackRF to 98.6 MHz. This would cause the station to appear
300 kHz below the center, so we would shift the specturm up by that
amount.

## Files summary

* **FM_Radio_rx.grc** can be used to find and listen to a Wideband FM station.
An antenna should be connected, and the RF amplifier may be needed to be enabled.
* **FM_tx_rx.grc** transmits a signal from one HackRF to another using FM modulation.
* **GFSK_tx_rx** transmits bits from one HackRF to another using GFSK.
* **GFSK_Heron_Packet_tx_rx.grc** transmits a packet in the required Heron format using GFSK
from one HackRF which is then received, demodulated, and decode by the other.
To find out more about the Heron format, checkout [this document](https://drive.google.com/file/d/1QbZfTUcGsZVrNnLC-i74AeppRjXvG178/view?usp=sharing).
