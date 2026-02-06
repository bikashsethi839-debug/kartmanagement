#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Kart Management Server..."
python app.py --no-https
