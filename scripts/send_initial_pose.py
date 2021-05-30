#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped

def talker():
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(1) # 10hz

	pose = PoseWithCovarianceStamped()

	pose.header.frame_id = "map"
	pose.pose.pose.position.x=-6.644
	pose.pose.pose.position.y=6.876
	pose.pose.pose.position.z=0
	pose.pose.covariance=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]
	pose.pose.pose.orientation.z=0.006
	pose.pose.pose.orientation.w=0.999641971333
	
	pub.publish(pose)
	rate.sleep()
	pub.publish(pose)
	rate.sleep()    
	pub.publish(pose)
	rate.sleep()
	
	rospy.loginfo(pose)
	#rospy.spin()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass