#!/bin/bash

echo "Starting desktop recorder at $(date)" >> /tmp/kelsa-desktop-recorder.log
cd /Users/prithvianilkumar/code/fun/kelsa/desktop-recorder
source /Users/prithvianilkumar/code/fun/kelsa/desktop-recorder/.env/bin/activate
pip install -e /Users/prithvianilkumar/code/fun/kelsa
exec python3 /Users/prithvianilkumar/code/fun/kelsa/desktop-recorder/main.py