#!/bin/bash

# Navigate to Choregraphe directory
cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64 || {
    echo "Choregraphe directory not found!"
    exit 1
}

# Run Choregraphe
echo "Starting Choregraphe..."
./choregraphe

