#!/bin/bash

cd ~/usage_monitor
source .venv/bin/activate
python -m client.main localhost
echo "Client exited. Press Enter to close..."
read