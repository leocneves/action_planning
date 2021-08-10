#Create new session. I named this LeftMonitor for obvious reasons
byobu new-session -d -s LeftMonitor

#Select default pane. Probably an unnecessary line of code
byobu select-pane -t 0

#Split pane 0 into two vertically stacked panes
byobu split-window -v

#Select the newly created pane 1. Again, probably unnecessary as the new pane gets selected after a split
byobu select-pane -t 1

#Split pane 1 horizontally to create two side-by-side panes
byobu split-window -h

#Repeat the selection and splitting process with the top half
byobu select-pane -t 0
byobu split-window -h


byobu select-pane -t 3
byobu split-window -v

#Select pane to interact with
byobu select-pane -t 0
byobu send-keys "roslaunch action_planning hera_plan_main.launch" Enter

byobu select-pane -t 1
byobu send-keys "rosrun action_planning text_to_fluent.py" Enter

byobu select-pane -t 2
byobu send-keys "roslaunch action_planning generate_plan.launch"

byobu select-pane -t 3
byobu send-keys "rostopic pub /command std_msgs/String \"data: 'Move to the bench, move to the bookshelf, and move to the bar.'\" "

byobu select-pane -t 4
byobu send-keys "rostopic pub /pnp/planToExec std_msgs/String \"data: 'plan'\" --once"

# kill-server // CTRL + F6


#Finally, to be able to actually see anything, you need to launch a terminal for each session --full-screen
gnome-terminal --full-screen -- byobu attach -t LeftMonitor
