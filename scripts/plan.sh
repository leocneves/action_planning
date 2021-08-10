#!/bin/bash
echo "Calling problem generator.";
rosservice call --wait /rosplan_problem_interface/problem_generation_server;
sleep 2;

echo "Calling planner interface.";
rosservice call --wait /rosplan_planner_interface/planning_server;
sleep 10;

echo "Parsing Plan.";
rosservice call --wait /rosplan_parsing_interface/parse_plan;
sleep 2;

# echo "Dispatching Plan.";
# rosservice call /rosplan_plan_dispatcher/dispatch_plan;

rosrun action_planning get_plan.py
# sleep 4
# #
# rostopic pub /pnp/planToExec std_msgs/String "data: 'plan'" --once
