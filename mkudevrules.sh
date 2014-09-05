#!/bin/sh
sudo sh -c 'cat > /etc/udev/rules.d/49-moz-amp.rules' <<EOF
# Ammeter
ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="204b", ENV{ID_MM_DEVICE_IGNORE}="1"
ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="204b", ENV{MTP_NO_PROBE}="1"
SUBSYSTEM=="tty", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="204b", MODE="0666", GROUP="dialout"

# Bootloader
ATTRS{idVendor}=="239a", ATTRS{idProduct}=="0001", ENV{ID_MM_DEVICE_IGNORE}="1"
ATTRS{idVendor}=="239a", ATTRS{idProduct}=="0001", ENV{MTP_NO_PROBE}="1"
SUBSYSTEM=="tty", ATTRS{idVendor}=="239a", ATTRS{idProduct}=="0001", MODE="0666", GROUP="dialout"
EOF
sudo udevadm control --reload-rules

