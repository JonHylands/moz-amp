#!/bin/sh

sudo sh -c 'cat > /etc/udev/rules.d/ammeter.rules' <<EOF
SUBSYSTEM=="tty", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="204b", MODE="0666", GROUP="dialout"
EOF

sudo udevadm control --reload-rules
