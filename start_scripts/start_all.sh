#!/bin/bash

# Navigate to Choregraphe directory
cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64 || {
    echo "Choregraphe directory not found!"
    exit 1
}

# Run Choregraphe
echo "Starting Choregraphe..."
./choregraphe > /dev/null 2>&1 &

# Open the GUI in Firefox
firefox ~/playground/nursing_app/index.html > /dev/null 2>&1 &

# Start MODIM WebSocket server in a new terminal with an internal 2-second delay
xterm -hold -e "sleep 1 && cd ~/playground/nursing_app/scripts/ && python start_interaction.py" &


# Navigate to the MODIM GUI directory
cd ~/playground/nursing_app/scripts/modim/ || {
    echo "MODIM GUI directory not found!"
    exit 1
}

# Run the WebSocket server in the background (interactive)
echo "Starting MODIM WebSocket server for 'pepper'..."
python ws_server.py -robot pepper

