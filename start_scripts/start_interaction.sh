#!/bin/bash

# Navigate to the interaction script directory
cd ~/playground/nursing_app/scripts/ || {
  echo "Directory not found!"
  exit 1
}

# Start the interaction Python script
python start_interaction.py

