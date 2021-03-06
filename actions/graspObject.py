import time
import threading
import rospy

# from abc import ABCMeta, abstractmethod
from pnp_msgs.msg import PNPActionFeedback, PNPResult

class graspObject():
    # __metaclass__ = ABCMeta

    def __init__(self, goalhandler, params):
        self.goalhandler = goalhandler
        self.params = params.split("_")
        self.done = False

        # create event for stopping the action
        self.cancel_event = threading.Event()

    # @abstractmethod
    def _start_action(self):
        rospy.logwarn("Pegando objeto %s de %s ..." % str(self.params[-2]),str(self.params[-1]))
        time.sleep(5)

        self.done = True
        # raise NotImplementedError()

    # @abstractmethod
    def _stop_action(self):
        rospy.loginfo('Stoping ...')
        # raise NotImplementedError()

    # @abstractmethod
    def _is_action_done(self):
        if self.done:
            rospy.loginfo('Done!')
            return True
        else:
            return False
        # raise NotImplementedError()

    ## main execution thread
    def _actionThread_exec(self):
        feedback = PNPActionFeedback()
        result = PNPResult()

        self._start_action()

        # wait until the action is done
        while not self._is_action_done():
            # request to cancel action
            if self.cancel_event.isSet():
                self._stop_action()
                break

            # send feedback
            feedback.feedback = 'running ...'
            self.goalhandler.publish_feedback(feedback)

            time.sleep(0.5)

        # send the result
        result.result = 'OK'
        self.goalhandler.set_succeeded(result, 'OK')

    def start_action(self):
        th = threading.Thread(None, self._actionThread_exec, args=())
        th.start()

    def stop_action(self):
        self.cancel_event.set()
