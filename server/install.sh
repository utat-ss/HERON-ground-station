#!/usr/bin/env bash 

id -u heron &>/dev/null || sudo useradd -r -s /bin/false heron
sudo systemctl stop doppler || true
sudo systemctl disable doppler || true
sudo systemctl stop HERON_gs || true
sudo systemctl disable HERON_gs || true

mkdir -p build && cd build
cmake ..
cpack -G DEB
sudo dpkg -i *.deb

sudo systemctl daemon-reload
sudo systemctl enable doppler
sudo systemctl start doppler
# sudo systemctl enable HERON_gs
# sudo systemctl start HERON_gs
