# Ground Station Software

Software that communicates with Heron Mk. II

## transceivers/ 

Contains gnuradio flowgraphs that behave as transceivers that can communicate with Heron Mk II. However, the code in this folder is ground station hardware dependent, specifically for the UTAT Heron Mk. II ground station and the UTAT RF Testbench.

Code to communicate with Heron Mk. II that is meant to be independent of ground station hardware choices are in the [HERON-gr-utat](https://github.com/utat-ss/HERON-gr-utat) repository. This enables code sharing so that if another ground station needs to be made that can talk to Heron Mk. II, it can be designed using gnuradio blocks in [HERON-gr-utat](https://github.com/utat-ss/HERON-gr-utat) while using the flowgraphs here as a template or example.

## tests/

Contains ground station specific tests. It is meant to check connectivity between the Heron Mk. II ground station and the RF Testbench in the UTAT Lab.

## pending_review/

This repository and the whole ground station architecture at UTAT is going through a massive renovation. All previous code that has not been tested, integrated into the new architecture, or reviewed by the current maintainers are in this folder. Any help to empty this folder is always appreciated!