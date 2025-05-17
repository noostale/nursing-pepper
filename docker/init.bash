#!/bin/bash

SESSION=init

tmux -2 new-session -d -s $SESSION

tmux rename-window -t $SESSION:0 'naoqi'
tmux new-window -t $SESSION:1 -n 'choregraphe'
tmux new-window -t $SESSION:2 -n 'pepper_tools'
tmux new-window -t $SESSION:3 -n 'modim'
tmux new-window -t $SESSION:4 -n 'playground'

tmux send-keys -t $SESSION:0 "cd /opt/Aldebaran/naoqi-sdk-2.5.7.1-linux64" C-m
tmux send-keys -t $SESSION:0 "./naoqi"

tmux send-keys -t $SESSION:1 "cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64" C-m
tmux send-keys -t $SESSION:1 "./choregraphe"

tmux send-keys -t $SESSION:2 "cd src/pepper_tools" C-m

tmux send-keys -t $SESSION:3 "cd ~/src/modim/src/GUI" C-m
tmux send-keys -t $SESSION:3 "python ws_server.py -robot pepper"

tmux send-keys -t $SESSION:4 "cd ~/playground/start_scripts" C-m
tmux send-keys -t $SESSION:4 "./start_all.sh"



while [ 1 ]; do
  sleep 60;
done


