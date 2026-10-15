import rclpy

from geometry_msgs.msg import Twist
def move_robot(direction: str, mvtime: int):
    msg = Twist()
    speeds = {
        "forward": (0.15, 0.0),
        "backward": (-0.15, 0.0),
        "left": (0.0, 0.4),
        "right": (0.0, -0.4),
        "stop": (0.0, 0.0),
    }

    # temp speeds, need to be tested.

    if direction not in speeds:
        return {"error": "invalid direction"}

    mvtime = max(0.0, min(mvtime, 1.0))

    linear, angular = speeds[direction]
    msg.angular=angular
    msg.linear=linear
    print(f"TEST: {direction}, {mvtime}s, linear: {linear}, angular: {angular}, msg: {msg}")
    return {"test_run": True, "direction": direction}