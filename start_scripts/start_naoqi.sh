#!/bin/bash

# Navigate to NAOqi SDK directory
cd /opt/Aldebaran/naoqi-sdk-2.5.7.1-linux64 || {
    echo "Failed to find NAOqi SDK directory!"
    exit 1
}

# Launch NAOqi binary
echo "Starting NAOqi..."
./naoqi

