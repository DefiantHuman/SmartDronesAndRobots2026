import time, math
from gz.msgs10.twist_pb2 import Twist
from gz.msgs10.image_pb2 import Image
from gz.msgs10.odometry_pb2 import Odometry
from gz.transport13 import Node

target_speed, actual_speed, current_yaw = 0.25, 0.0, 0.0
adaptive_push, surface, sim_active = 0.0, "TILE", False

def odom_cb(msg):
    global actual_speed, current_yaw, sim_active
    actual_speed = msg.twist.linear.x
    o = msg.pose.orientation
    current_yaw = math.atan2(2.0*(o.w*o.z + o.x*o.y), 1.0 - 2.0*(o.y*o.y + o.z*o.z))
    sim_active = True

def camera_cb(msg):
    global surface
    try:
        avg = sum(list(msg.data)) / len(msg.data)
        surface = "TILE" if avg > 150 else "CARPET"
    except: pass

node = Node()
pub = node.advertise('/cmd_vel', Twist)
node.subscribe(Image, '/camera/image_raw', camera_cb)
node.subscribe(Odometry, '/model/bot_v2/odometry', odom_cb)

while True:
    if sim_active:
        # SPEED: High gain (0.05) makes the speed recovery very visible
        if surface == "CARPET" and (target_speed - actual_speed) > 0.01:
            adaptive_push += 0.05 
        elif surface == "TILE":
            adaptive_push = 0.0

        # STEERING: Very high gain (12.0) to fight the 'Split' spin
        steering = (0.0 - current_yaw) * 12.0 

        msg = Twist()
        msg.linear.x = target_speed + adaptive_push
        msg.angular.z = steering
        pub.publish(msg)
        print(f"[{surface}] Spd: {actual_speed:.2f} | Push: +{adaptive_push:.2f} | Yaw: {math.degrees(current_yaw):.1f}")
    time.sleep(0.1)