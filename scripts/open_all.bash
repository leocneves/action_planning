#!/bin/sh

roslaunch action_planning test_pizza.launch

rostopic echo /rosplan_plan_dispatcher/action_dispatch

rosrun action_planning plan.bash

roslaunch rosplan_planning_system simulated_action.launch pddl_action_name:='goto_waypoint'
