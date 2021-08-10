#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from rosplan_dispatch_msgs.msg import CompletePlan
import time
import os

global pub

def callback(data):
    global pub
    s = []
    for act in data.plan:
        if act.name == 'wait': continue

        args = "_".join([x.value for x in act.parameters]) #  if x.key != 'r'
        if args != "":
            s.append(act.name + "_" + args)
        else:
            s.append(act.name)
    if len(s) > 0:

        final = ";\n".join(s)

        filePath = os.path.expanduser("~") + '/catkin_ws/src/action_planning/plans/'
        plan_name = 'plan'
        exec_rule_name = 'exec_rules'

        if os.path.exists(filePath + plan_name + '.txt'):
            os.remove(filePath + plan_name + '.txt')
        else:
            pass

        with open(filePath + plan_name + '.txt', 'w') as file:
            file.write(final)
            file.close()

        try:
            os.system(f'cd {filePath} & pnpgen_linear {filePath + plan_name + ".txt"} {filePath + exec_rule_name + ".er"}')
            rospy.loginfo("Plan generated!")
        except Exception as e:
            print(e)

        # pub.publish(final)
        # time.sleep(0.3)
        # pub.publish(final)
        # rospy.loginfo(final)

def listener():
    global pub
    rospy.init_node('get_plan', anonymous=True)
    pub = rospy.Publisher('/kcl_rosplan/plan_graph', String, queue_size=10)
    rospy.Subscriber("/rosplan_parsing_interface/complete_plan", CompletePlan, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
