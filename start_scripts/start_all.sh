#!/bin/bash

####################################
##        NAOqi Launching        ##
####################################

# Navigate to the NAOqi SDK installation directory
cd /opt/Aldebaran/naoqi-sdk-2.5.7.1-linux64

# Launch the NAOqi executable using xterm and keep the terminal open
echo "Initializing NAOqi..."
xterm -fa Monospace -fs 10 -hold -e ./naoqi &

# Allow sufficient time for NAOqi to start and stabilize
echo "Waiting for NAOqi initialization..."
sleep 5


####################################
##      Choregraphe Launching     ##
####################################

# Change directory to Choregraphe installation path
cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64

# Launch Choregraphe IDE silently in the background
echo "Launching Choregraphe environment..."
./choregraphe /home/robot/playground/start_scripts/pepper/pepper.pml > /dev/null 2>&1 &


####################################
##         Web GUI Launch         ##
####################################

# Open the local web interface using Firefox inside an xterm window
echo "Launching web interface in Firefox..."
xterm -fa Monospace -fs 10 -hold -e "firefox ~/playground/nursing_app/index.html" &


####################################
##     Interaction Script Start   ##
####################################

# Start the interaction Python script after a brief delay (ensures MODIM is running)
echo "Starting interaction script..."
xterm -fa Monospace -fs 10 -hold -e "sleep 1 && cd ~/playground/nursing_app/scripts/ && python rdf.py" &


####################################
##     MODIM Server Execution     ##
####################################

# Navigate to the MODIM server script directory
cd ~/playground/nursing_app/scripts/modim/

# Execute the MODIM WebSocket server in interactive mode for Pepper
echo "Launching MODIM WebSocket server for Pepper..."
python ws_server.py -robot pepper
