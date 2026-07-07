#!/bin/bash

cd ~/usage_monitor
source .venv/bin/activate
python -m server.main
echo "Server exited. Press Enter to close..."
read