import math
import sys
from cmath import acos

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# add additional
'''Intelligence gathering speed of pod - arbitary value derived from the distance from last sample - done rate toward 
target - speed toward next checkpoint - done implement telemetry improve speed function implement will_hit_target - 
iteration 1:  will the pod be facing the target by the time it reaches it given that we know distance and ticks and 
acceleration is about 25 per tick and the turn rate is 17 degrees a tick the algorithm would be the distance to the 
target and the starting speed and angle add additional telemetry to determine turn rate is it constant - NO add code 
to decelerate and accelerate - Done Implement trajectorey angle as simple response - done implement apex points '''


def debug(m):
    print(m, file=sys.stderr, flush=True)


def distance_between_two_points(reference_x, reference_y, target_x, target_y):
    x_delta = target_x - reference_x
    y_delta = target_y - reference_y
    return int(math.sqrt((x_delta ** 2) + (y_delta ** 2)))

def distance_between_coords(source_checkpoint, target_checkpoint):
    source_checkpoint.update_distance_to_next(target_checkpoint.x, target_checkpoint.y)

def calculate_angles_from_coords(point_a_x, point_a_y, point_b_x, point_b_y, point_c_x, point_c_y):
    try:
        debug(f"point a {point_a_x}:{point_a_y}, point b {point_b_x}:{point_b_y}, point c {point_c_x}:{point_c_y}")
        side_a = distance_between_two_points(point_a_x, point_a_y, point_b_x, point_b_y)
        side_b = distance_between_two_points(point_b_x, point_b_y, point_c_x, point_c_y)
        side_c = distance_between_two_points(point_c_x, point_c_y, point_a_x, point_a_y)
        angle_a = acos((side_b ** 2 + side_c ** 2 - side_a ** 2) / (2 * side_b * side_c)).real
        angle_b = acos((side_a ** 2 + side_c ** 2 - side_b ** 2) / (2 * side_a * side_c)).real
        angle_c = acos((side_a ** 2 + side_b ** 2 - side_c ** 2) / (2 * side_a * side_b)).real
        a_as_degrees = round(57.29 * angle_a, 0)
        b_as_degrees = round(57.29 * angle_b, 0)
        c_as_degrees = round(57.29 * angle_c, 0)
        return [a_as_degrees, b_as_degrees, c_as_degrees]
    except Exception as e:
        debug(f" {e} ")

def map_checkpoint(previous_checkpoint, current_checkpoint, next_checkpoint):
    current_checkpoint.update_distance_to_next(next_checkpoint.x, next_checkpoint.y)
    current_checkpoint.apex_angle = \
        calculate_angles_from_coords(previous_checkpoint.x, previous_checkpoint.y, current_checkpoint.x,
                                     current_checkpoint.y, next_checkpoint.x, next_checkpoint.y)[0]

def calculate_trajectory(primary_x, primary_y, secondary_x, secondary_y, target_x, target_y):
    reference_line = distance_between_two_points(primary_x, primary_y, target_x, target_y)
    travel_line = distance_between_two_points(primary_x, primary_y, secondary_x, secondary_y)
    target_line = distance_between_two_points(secondary_x, secondary_y, target_x, target_y)

    reference_angle = int(57.29 * (
        (acos((reference_line ** 2 + travel_line ** 2 - target_line ** 2) / (2 * reference_line * travel_line)).real)))
    travel_angle = int(57.29 * (
        acos((travel_line ** 2 + target_line ** 2 - reference_line ** 2) / (2 * travel_line * target_line)).real))
    target_angle = int(57.29 * (
        acos((target_line ** 2 + reference_line ** 2 - travel_line ** 2) / (2 * target_line * reference_line)).real))
    return [reference_angle, travel_line, target_angle, travel_angle]

def will_pod_hit(refrence_x=None, secondary_x=None, secondary_y=None, target_x=None, target_y=None):
    # light weight check assumptions, accelleration is constant 25 per tick, max speed is 650, turnRate is 17 degrees
    # per tick v 1.2 - normalize to 360 degrees - done - redact for 1.3 v 1.3 - compensate for speed by reducing the
    # angle available as a factor of percent of max speed - fail cant detect miss in time v 1.4 - apply vector angles
    # and try and determine where it will go over the distance

    return True


class Checkpoint:
    def __init__(self, position, x_coord, y_coord):
        self.position = position
        self.x = x_coord
        self.y = y_coord
        self.distance_to_next = None
        self.apex_x = None
        self.apex_y = None
        self.angle_to_next = None

    def __str__(self):
        return f"{self.position}, {self.x}, {self.y}, {self.distance_to_next}"

    def update_distance_to_next(self, next_x, next_y):
        self.distance_to_next = distance_between_two_points(self.x, self.y, next_x, next_y)

    def set_angle_to_next(self, previous_checkpoint, next_checkpoint):
        trajectory_data = calculate_angles_from_coords(previous_checkpoint.x, previous_checkpoint.y, self.x, self.y,
                                                       next_checkpoint.x, next_checkpoint.y)
        self.angle_to_next = trajectory_data[0]


class Telemetry:
    def __init__(self):
        self.readings = []

    def add_reading(self, record):
        debug(record)
        self.readings.append(record)


class Course:
    def __init__(self):
        self.checkpoints = []
        self.course_known = False
        self.active_target_checkpoint = None
        self.last_active_checkpoint = None
        self.lap = 0
        self.longest_run_checkpoint = None


    def add_checkpoint(self, checkpoint_id, checkpoint_x, checkpoint_y):
        checkpoints.append(Checkpoint(checkpoint_id, checkpoint_x, checkpoint_y))

    def update_longest_run_checkpoint(self):
        lengths = [x.distance_to_next for x in self.checkpoints]
        lengths.insert(0, lengths.pop())
        self.longest_run_checkpoint = next(x for x in checkpoints if x.distance_to_next == max(lengths))



    def update_active_target(self, target_x, target_y):
        self.last_active_checkpoint = self.active_target_checkpoint
        self.update_course_state(target_x, target_y)
        self.active_target_checkpoint = (
            next((cp for cp in checkpoints if cp.x == target_x and cp.y == target_y), None))

    def add_checkpoint_check(self, next_checkpoint_x_coord, next_checkpoint_y_coord):
        checkpoints_changed = self.checkpoints[-1].x != next_checkpoint_x_coord or checkpoints[
            -1].y != next_checkpoint_y_coord
        checkpoint_matches_known = (sum(c.x == next_checkpoint_x_coord for c in checkpoints) > 0 and sum(
            c.y == next_checkpoint_y_coord for c in checkpoints) > 0)
        return checkpoints_changed and not checkpoint_matches_known

    def all_checkpoints_known_check(self, next_checkpoint_x_coord, next_checkpoint_y_coord):
        next_checkpoint_is_first = len(self.checkpoints) > 1 and self.checkpoints[0].x == next_checkpoint_x_coord and \
                                   self.checkpoints[0].y == next_checkpoint_y_coord
        return next_checkpoint_is_first

    def update_course_state(self, next_checkpoint_x_coord, next_checkpoint_y_coord):
        if self.add_checkpoint_check(next_checkpoint_x_coord, next_checkpoint_y_coord):
            selected_target = Checkpoint(len(self.checkpoints) + 1, next_checkpoint_x_coord, next_checkpoint_y_coord)
            checkpoints.append(selected_target)
            for c in self.checkpoints:
                debug(c)

        if self.active_target_checkpoint != self.last_active_checkpoint and self.active_target_checkpoint == \
                course.checkpoints[1]:
            self.lap += 1
            debug(f"Lap changed, lap {self.lap}")

        elif self.all_checkpoints_known_check(next_checkpoint_x_coord, next_checkpoint_y_coord):  # set checkpoints
            debug("Map read executing analysis")
            for c_index in range(len(self.checkpoints)):
                self.update_checkpoint_to_checkpoint_angle(c_index)

            for c in self.checkpoints:
                debug(c)
            self.course_known = True

            self.update_longest_run_checkpoint()




    def update_checkpoint_to_checkpoint_angle(self, c_index):
        target_checkpoint_index = c_index + 1 if c_index + 1 < len(self.checkpoints) else 0
        distance_between_coords(self.checkpoints[c_index - 1], self.checkpoints[c_index])
        debug(f"{c_index}, {target_checkpoint_index}")
        self.checkpoints[c_index].set_angle_to_next(self.checkpoints[c_index - 1],
                                                    self.checkpoints[target_checkpoint_index])


class Pod:
    """
    Independent analysis shows that the pod max acceleration is over 5 turns then slow but continual, max speed in 24
    turns with no influence from non linear momentum the pod turns 17 degrees per tick, validation = the calculated
    distance to target shall match reported  - passed
    """

    def __init__(self, identity, start_x, start_y, distance_to_target):
        self.identity = identity
        self.x = start_x
        self.y = start_y
        self.x_momentum = 0
        self.y_momentum = 0
        self.speed = 0
        self.target_distance = distance_to_target
        self.speed_to_target = 0
        self.tel = Telemetry()
        self.race_iterator = 0
        self.target_id = 1
        self.trajectory_angle = 0
        self.thrust = 100
        self.hit_next_target = True
        self.boost_fired = False
        self.angle_to_target = 0

    def update_position(self, target_id, new_x, new_y, distance_to_target, angle_to_target, target_x, target_y):
        self.race_iterator += 1
        self.update_speed(new_x, new_y)
        self.speed_to_target = self.target_distance - distance_to_target
        trajectory = calculate_trajectory(self.x, self.y, new_x, new_y, target_x, target_y)
        debug(trajectory)
        self.trajectory_angle = trajectory[0]
        self.update_pod_position(new_x, new_y)
        self.target_distance = distance_to_target
        self.angle_to_target = angle_to_target
        self.target_x = target_x
        self.target_y = target_y
        self.will_i_hit_target()
        debug(
            f"calculated distance to target {distance_between_two_points(self.x, self.y, target_x, target_y)}/"
            f" system distance {distance_to_target}")
        reading_data = {"race_iteration": self.race_iterator, "hit_target_indicator": self.hit_next_target,
                        "target_id": target_id, "pod_x": new_x, "pod_y": new_y, "angle_to_target": angle_to_target,
                        "distance_to_target": distance_to_target, "trajectory_angle": self.trajectory_angle,
                        "speed": self.speed, "speed_to_target": self.speed_to_target}
        self.tel.add_reading(reading_data)

    def update_speed(self, new_x, new_y):
        self.x_momentum = (self.x - new_x) * -1
        self.y_momentum = (self.y - new_y) * -1
        self.speed = distance_between_two_points(self.x, self.y, new_x, new_y)

    def update_pod_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def accellerate(self, rate):
        if (self.thrust + rate) > 100:
            self.thrust = 100
        else:
            self.thrust += rate

    def decellerate(self, rate):
        if (self.thrust - rate) < 5:
            self.thrust = 5
        else:
            self.thrust -= rate

    def will_i_hit_target(self):
        self.hit_next_target = True if (self.trajectory_angle in range(0, 15) or self.angle_to_target < 20) else False

    def __str__(self):
        return (
            f"pod {self.identity} Speed {self.speed} Speed to target {self.speed_to_target},/"
            f" trajectory angle to target {self.trajectory_angle}, thrust {self.thrust}, /"
            f"hit target {self.hit_next_target}, angletoTarget {self.angle_to_target}")


class Pilot:
    def __init__(self, course, pod):
        self.course = course
        self.pod = pod

    def get_decision(self):
        if self.course.course_known:
            return f"{self.course.active_target_checkpoint.x} {self.course.active_target_checkpoint.y} {self.thrust_value()}"
        else:
            return f"{self.course.active_target_checkpoint.x} {self.course.active_target_checkpoint.y} {self.thrust_value()}"

    def thrust_value(self):
        if self.fire_boost_check():
            return "BOOST"
        else:
            return "100"



    def fire_boost_check(self):
        if not self.pod.boost_fired:
            if (self.course.active_target_checkpoint == self.course.longest_run_checkpoint):
                self.pod.boost_fired = True
                return True
        else:
            return False

'''Operational race code'''

pods = []
active_target = None
course_known = False
boost_fired = False
lap = 1
lapped = False
course = Course()
checkpoints = course.checkpoints
pod_action = None
pilot = None

def update_pod_telemetry(player_pod, next_checkpoint_angle):
    # next_checkpoint_angle = distance_between_two_points(x, y, next_checkpoint_x, next_checkpoint_y)
    player_pod.update_position(course.active_target_checkpoint.position, x, y, next_checkpoint_dist,
                               next_checkpoint_angle, next_checkpoint_x, next_checkpoint_y)
    debug(f"{pods[0]}")
    return pods[0]


# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint

    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    if len(checkpoints) == 0:  # no checkpoints add one
        course.add_checkpoint(1, next_checkpoint_x, next_checkpoint_y)
        pods.append(Pod("Player", x, y, next_checkpoint_dist))
        pilot = Pilot(course, pods[0])

    course.update_active_target(next_checkpoint_x, next_checkpoint_y)

    if pilot.pod.x != x or pilot.pod.y != y:  # is the pod in a different positon to last time
        update_pod_telemetry(pilot.pod, next_checkpoint_angle)

    pod_action = pilot.get_decision()
    debug(pod_action)
    '''   if course.course_known:

        pilot.course.update_active_target(next_checkpoint_x, next_checkpoint_y)

        player.decellerate(40) if not player.hit_next_target else player.accellerate(60)

        if not boost_fired and course.active_target_checkpoint.position == course.longest_run_checkpoint:
            if player.trajectory_angle <= 30:
                debug("Fire boost")
                player.fire_boost = True
                boost_fired = True
    else:
        player.decellerate(40) if not player.hit_next_target else player.accellerate(60)

    debug(f"thrust {player.thrust}, boost fired {boost_fired}")'''

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"

    print(pod_action)
