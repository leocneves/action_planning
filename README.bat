roslaunch action_planning test_pizza.launch

rosrun action_planning plan.bash

roslaunch rosplan_planning_system simulated_action.launch pddl_action_name:='goto_waypoint'
