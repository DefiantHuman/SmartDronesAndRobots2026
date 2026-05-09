import time
from gz.msgs10.twist_pb2 import Twist
from gz.transport13 import Node

node = Node()
pub = node.advertise('/cmd_vel', Twist)

print("RECORDING: DUMB MODE. No sensors, no correction.")
while True:
    msg = Twist()
    msg.linear.x = 0.25 # Constant effort
    pub.publish(msg)
    time.sleep(0.1)