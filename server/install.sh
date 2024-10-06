#!/usr/bin/env bash 

id -u heron &>/dev/null || sudo useradd -r -s /bin/false heron

mkdir -p build && cd build
cmake ..
cpack -G DEB
sudo dpkg -i *.deb

sudo systemctl daemon-reload
sudo systemctl enable doppler
sudo systemctl start doppler
sudo systemctl enable HERON_gs
sudo systemctl start HERON_gs
