#!/bin/bash

cd ~/usage_monitor
source .venv/bin/activate
read -p "Server IP: " SERVER_IP
python -m client.main "$SERVER_IP"
echo "Client exited. Press Enter to close..."
read