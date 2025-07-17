#!/bin/bash

# Lightweight IoT Blockchain Installer
# For Raspberry Pi and similar devices

echo "Installing dependencies..."
sudo apt update
sudo apt install -y \
    python3-pip \
    mosquitto \
    libatlas-base-dev  # For numpy dependencies

echo "Installing Python packages..."
pip3 install -r requirements.txt --no-cache-dir

echo "Configuring MQTT broker..."
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

echo "Setting up as IoT device..."
cat > /etc/systemd/system/iot-blockchain.service <<EOF
[Unit]
Description=IoT Blockchain Device
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/iot_blockchain_project/edge_layer/device.py
WorkingDirectory=/home/pi/iot_blockchain_project
User=pi
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable iot-blockchain
sudo systemctl start iot-blockchain

echo "Installation complete!"