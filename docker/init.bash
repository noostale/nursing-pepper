#!/bin/bash

SESSION="start_env"
SCRIPT_DIR=~/playground/start_scripts

# Start a new tmux session in detached mode
tmux new-session -d -s $SESSION -c $SCRIPT_DIR

# Pane 0: Run start_naoqi.sh
tmux send-keys -t $SESSION "bash $SCRIPT_DIR/start_naoqi.sh" C-m

# Split vertically and run start_modim_ws.sh
tmux split-window -v -t $SESSION -c $SCRIPT_DIR
tmux send-keys -t $SESSION "bash $SCRIPT_DIR/start_modim_ws.sh" C-m

# Split horizontally from top pane (0) and run start_interaction.sh
tmux select-pane -t $SESSION:.0
tmux split-window -h -t $SESSION -c $SCRIPT_DIR
tmux send-keys -t $SESSION "bash $SCRIPT_DIR/start_interaction.sh" C-m

# Select bottom pane (1) and split it horizontally too
tmux select-pane -t $SESSION:.1
tmux split-window -h -t $SESSION -c $SCRIPT_DIR
tmux send-keys -t $SESSION "bash $SCRIPT_DIR/start_firefox.sh" C-m

# Select one pane (e.g., 3) and run start_choregraphe.sh
tmux select-pane -t $SESSION:.3
tmux split-window -v -t $SESSION -c $SCRIPT_DIR
tmux send-keys -t $SESSION "bash $SCRIPT_DIR/start_choregraphe.sh" C-m

# Attach to the session
tmux attach -t $SESSION
