import time
import RPi.GPIO as GPIO # Raspberry Pi I/O library
import threading
from math import cos, sin, atan2, sqrt, pi # For polar conversion.
from polar import *
from queue import Queue


# CURRENTLY ASSUMING:
#   Motor 1 is set up as R.
#   Motor 2 is set up as Theta.
#   Motor 3 is set up as Z.
#   Clockwise rotation always results in a move towards (0, 0, 0)

# Current set up of motor steps.

#     Pin 1   Pin 2   Pin 3   Pin 4
#  1    x
#  2    x       x
#  3            x
#  4            x       x
#  5                    x
#  6                    x      x
#  7                           x
#  8    x                      x



# Define the number of steps for the motor
# to complete a single full rotation.
FULL_CIRCLE = 510.0

# Number of millimeters per step for DR and DZ.
# Amount of radians per one step for DTHETA
STEPS_PER_MM_DZ = 0.0062
STEPS_PER_RAD_DT = 0.00147
STEPS_PER_MM_DR = 0.123

# Inverse relations.
DZ_TO_STEPS_PER_MM = 1 / STEPS_PER_MM_DZ
DT_TO_STEPS_PER_RAD = 1 / STEPS_PER_RAD_DT
DR_TO_STEPS_PER_MM = 1 / STEPS_PER_MM_DR


# --------------------------- REFACTOR -----------------------------------------


class Motor(object):



    # ------------------- Set up ---------------------


    def __init__(self):
        # Set up for the Raspberry Pi
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        for i in range(1, 4):
            GPIO.setup(self.get_channels(i), GPIO.OUT)


    def move(self, trajectory):
        # Move the platform, given a list of steps for each motor.
        threads = []
        r = Queue(maxsize = 0)
        t = Queue(maxsize = 0)
        z = Queue(maxsize = 0)
        r_worker = threading.Thread(target=self.move_r, args=(trajectory[0], r))
        theta_worker = threading.Thread(target=self.move_theta, args = (trajectory[1], t))
        z_worker = threading.Thread(target=self.move_z, args = (trajectory[2], z))
        threads.append(r_worker)
        threads.append(theta_worker)
        threads.append(z_worker)

        for thread in threads:
            thread.start()
            print("start")

        for thread in threads:
            thread.join()
            print("join")

        return [r.get(), t.get(), z.get()]

        # for steps in trajectory:
        #     self.move_r(steps[0])
        #     self.move_theta([steps[1]])
        #     self.move_z([steps[2]])


    def move_r(self, steps, q):
        # Move the R motor.
        r = []
        channel = self.get_channels(1)
        if steps > 0:
            r = self._counter_turn(channel, abs(steps), r)
        else:
            self._clockwise_turn(channel, abs(steps), r)
        q.put(r)


    def move_theta(self, steps, q):
        # Move the theta motor.
        t = []
        channel = self.get_channels(2)
        if steps < 0:
            t = self._counter_turn(channel, abs(steps), t)
        else:
            t = self._clockwise_turn(channel, abs(steps), t)
        q.put(t)


    def move_z(self, steps, q):
        # Move the Z motor.
        z = []
        channel = self.get_channels(3)
        if steps > 0:
            z = self._counter_turn(channel, abs(steps), z)
        else:
            z = self._clockwise_turn(channel, abs(steps), z)
        q.put(z)


    def get_channels(self, motor):
            # Return the appropriate control channels
            # based on which motor is specified.
            if motor == 1:
                return [7, 11, 13, 15]
            elif motor == 2:
                return [12, 16, 18, 22]
            else: # Motor 3.
                return [29, 31, 33, 35]


    def get_motor(self, chan):
        if chan == [7, 11, 13, 15]:
            return 1
        elif chan == [12, 16, 18, 22]:
            return 2
        else:
            return 3


    def run(self, num_steps, channels, direction):
        # Target for the worker threads.
        if direction == 'clock':
            self._clockwise_turn(channels, num_steps)
        else: # direction == 'counter'
            self._counter_turn(channels, num_steps)


    def get_steps(self, delta, conversion):
        # Returns the number of steps the motor should
        # take to achieve the given delta.
        return delta * conversion


    def _gpio_setup(self, channels, inputs):
            # Loop through the two lists simultaneously,
            # and apply the motor changes to each channel.
            for chan, step in zip(channels, inputs):
                GPIO.output(chan, step)
            # Allow motor to receive instructions
            time.sleep(0.0008)


    def _clockwise_turn(self, channels, steps, vec):
        # Turn the given motor right by a given number of degrees.
        if self.get_motor(channels) == 1:
            inc = 0.123
        elif self.get_motor(channels) == 2:
            inc = 0.00147
        else:
            inc = 0
        vec.append(0)
        self._gpio_setup(channels, [0, 0, 0, 0])
        self._gpio_setup(channels, [1, 0, 0, 0])
        current_step = [1, 0, 0, 0]

        while steps > 0.0:
            current_step = self._get_next_counter(current_step)
            self._gpio_setup(channels, current_step)
            steps -= 1
            vec.append(vec[-1] + inc)

        self._gpio_setup(channels, [0, 0, 0, 0])
        return vec


    def _counter_turn(self, channels, steps, vec):
        # Turn the given motor left by a given number of degrees.
        if self.get_motor(channels) == 1:
            inc = 0.123
        elif self.get_motor(channels) == 2:
            inc = 0.00147
        else:
            inc = 0
        vec.append(0)
        self._gpio_setup(channels, [0, 0, 0, 0])
        self._gpio_setup(channels, [1, 0, 0, 1])
        current_step = [1, 0, 0, 1]

        while steps > 0.0:
            current_step = self._get_next_counter(current_step)
            self._gpio_setup(channels, current_step)
            steps -= 1
            vec.append(vec[-1] + inc)

        self._gpio_setup(channels, [0, 0, 0, 0])
        return vec


    def _get_next_clock(self, current_step):
        # Big ugly function brute forcing the steps.  Find a better way!
        if current_step == [1, 0, 0, 0]:
            return [1, 1, 0, 0]
        elif current_step == [1, 1, 0, 0]:
            return [0, 1, 0, 0]
        elif current_step == [0, 1, 0, 0]:
            return [0, 1, 1, 0]
        elif current_step == [0, 1, 1, 0]:
            return [0, 0, 1, 0]
        elif current_step == [0, 0, 1, 0]:
            return [0, 0, 1, 1]
        elif current_step == [0, 0, 1, 1]:
            return [0, 0, 0, 1]
        elif current_step == [0, 0, 0, 1]:
            return [1, 0, 0, 1]
        else: # current_step == [1, 0, 0, 1]
            return [1, 0, 0, 0]


    def _get_next_counter(self, current_step):
        # Big ugly function brute forcing the steps.  Find a better way!
        if current_step == [1, 0, 0, 1]:
            return [0, 0, 0, 1]
        elif current_step == [0, 0, 0, 1]:
            return [0, 0, 1, 1]
        elif current_step == [0, 0, 1, 1]:
            return [0, 0, 1, 0]
        elif current_step == [0, 0, 1, 0]:
            return [0, 1, 1, 0]
        elif current_step == [0, 1, 1, 0]:
            return [0, 1, 0, 0]
        elif current_step == [0, 1, 0, 0]:
            return [1, 1, 0, 0]
        elif current_step == [1, 1, 0, 0]:
            return [1, 0, 0, 0]
        else: # current_step == [1, 0, 0, 0]
            return [1, 0, 0, 1]




    # def move(self, deltas):
    #     threads = self.get_threads(deltas)
    #
    #     for thread in threads:
    #         thread.start()
    #
    #     for thread in threads:
    #         thread.join()




    # def get_threads(self, deltas):
    #     threads = []
    #     # Get threads to move the motors
    #     if deltas[0] != 0:
    #         # Get the correct motor channels.
    #         channels = self.get_channels(1)
    #         if deltas[0] < 0:
    #             # Turn clockwise.
    #             direction = 'clock'
    #         else:
    #             direction = 'counter'
    #         r_steps = self.get_steps(deltas[0], DR_TO_STEPS_PER_MM)
    #         r_worker = self.get_worker(r_steps, channels, direction)
    #         threads.append(r_worker)
    #     if deltas[1] != 0:
    #         channels = self.get_channels(2)
    #         if deltas[1] > 0:
    #             direction = 'clock'
    #         else:
    #             direction = 'counter'
    #         theta_steps = self.get_steps(deltas[1], DT_TO_STEPS_PER_RAD)
    #         theta_worker = self.get_worker(theta_steps, channels, direction)
    #         threads.append(theta_worker)
    #     if deltas[2] != 0:
    #         channels = self.get_channels(2)
    #         if deltas[2] < 0:
    #             direction = 'clock'
    #         else:
    #             direction = 'counter'
    #         z_steps = self.get_steps(deltas[2], DZ_TO_STEPS_PER_MM)
    #         z_worker = self.get_worker(z_steps, channels, direction)
    #         threads.append(z_worker)
    #
    #     return threads





    # def get_worker(self, steps, channels, direct):
    #     # Returns a worker thread to move a single motor.
    #     return threading.Thread(target = self.run, args=(steps, channels, direct))




    # def platform_phone_home(self, current):
    #     # Go to the REAL origin. (Theta is forced to 0 as well).
    #     origin_deltas = [
    #         current[0] * -1,
    #         current[1] * -1,
    #         0
    #     ]
    #     print("Going home!")
    #     self.move(origin_deltas)






# --------------------------- REFACTOR -----------------------------------------

#
# class CameraMotor():
#     # A multithreaded component that operates
#     # stepper motors to control the camera.
#     # Given the rectangular coordinates of where to move,
#     # the class will be able to get there.
#
#     def __init__(self, current_coords):
#         # current_coords: a dictionary of three recatangular
#         # coordinates describing where the camera is currently.
#
#         # Amount of steps in the motors circle.
#         self.FULL_CIRCLE = 510.0
#
#         self.current = self._convert_to_polar(current_coords)
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setwarnings(False)
#
#         for i in range(1, 4):
#             GPIO.setup(self.get_channels(i), GPIO.OUT)
#
#
#
# # ------------------ Unit Conversions -----------------------------------------
#
#
#     def _convert_to_polar(self, cords):
#         new_cords = {}
#         # Get R in polar.
#         x_square = cords['x'] ** 2
#         y_square = cords['y'] ** 2
#         new_cords['r'] = sqrt(x_square + y_square) * self.FULL_CIRCLE
#         # Get theta in polar.
#         new_cords['theta'] = atan2(cords['y'], cords['x']) * (self.FULL_CIRCLE/2)
#         # We get Z for free!
#         new_cords['z'] = cords['z'] * self.FULL_CIRCLE
#         return new_cords
#
#
#     def _convert_to_cartesian(self, polar):
#         new_cords = {}
#         new_cords['x'] = (polar['r'] * cos(polar['theta'])) / self.FULL_CIRCLE
#         new_cords['y'] = (polar['r'] * sin(polar['theta'])) / self.FULL_CIRCLE
#         new_cords['z'] = polar['z'] / self.FULL_CIRCLE
#         return new_cords
#
#
#
# # ------------------ Motor Movement -------------------------------------------
#
#
#     def move(self, coords):
#         threads = []
#         polar = self._convert_to_polar(coords)
#
#         for cord, pos in self.current.items():
#             # Get worker threads for which ever motors
#             # need to be moved to get to the next position.
#             if polar[cord] != self.current[cord]:
#                 worker = self._get_worker(cord, polar)
#                 threads.append(worker)
#
#         # Start all of the worker threads.
#         for worker in threads:
#             worker.start()
#
#         # Wait for all of the worker threads to finish their tasks.
#         for worker in threads:
#             worker.join()
#
#         # Success! We moved!
#         self.current = polar
#         return self._convert_to_cartesian(self.current)
#
#
#     def _get_worker(self, cord, polar):
#         # Cord: a string containing either 'r', 'theta', or 'z'.
#         # Polar: a dictionary containing the three coordinates.
#         # Motor: an int describing which set of Pi channels to use.
#         #   Either 1, 2, or 3.
#         dest = polar[cord] - self.current[cord]
#         if cord == 'r' or cord == 'z':
#             if cord == 'r':
#                 channels = self.get_channels(1)
#             else:
#                 channels = self.get_channels(3)
#             if polar[cord] < self.current[cord]:
#                 # Spin the motor so it moves towards (0, 0, 0).
#                 direct = 'clock'
#             else:
#                 # Otherwise, spin it so it moves away from the origin.
#                 direct = 'counter'
#         else: # cord == 'theta'
#             channels = self.get_channels(2)
#             distance = self.current[cord] - polar[cord]
#             if distance < 0.0: # Move clockwise.
#                 direct = 'clock'
#             else: # Move counter clockwise.
#                 direct = 'counter'
#             dest = abs(dest)
#
#         # Designate a worker thread to handle the move.
#         worker = threading.Thread(target=self._run, args=(dest, channels, direct))
#         return worker
#
#
#     def get_channels(self, motor):
#         # Return the appropriate control channels
#         # based on which motor is specified.
#         if motor == 1:
#             return [7, 11, 13, 15]
#         elif motor == 2:
#             return [12, 16, 18, 22]
#         else: # Motor 3.
#             return [29, 31, 33, 35]
#
#
#     def _run(self, num_steps, channels, direction):
#         # Target for the worker threads.
#         if direction == 'clock':
#             self._clockwise_turn(channels, num_steps)
#         else: # direction == 'counter'
#             self._counter_turn(channels, num_steps)
#
#
#     def get_location(self):
#         return self._convert_to_cartesian(self.current)
#
#
#     def _get_steps(self, rad):
#         # Return the amount of steps required to
#         # turn the given amount of degrees.
#         return (self.FULL_CIRCLE/360.0) * rad
#
#
#     def _gpio_setup(self, channels, inputs):
#         # Loop through the two lists simultaneously,
#         # and apply the motor changes to each channel.
#         for chan, step in zip(channels, inputs):
#             GPIO.output(chan, step)
#         # Allow motor to catch up?
#         time.sleep(0.001)
#
#
#     def _clockwise_turn(self, channels, steps):
#         # Turn the given motor right by a given number of degrees.
#         #steps = get_steps(deg)
#         self._gpio_setup(channels, [0, 0, 0, 0])
#         self._gpio_setup(channels, [1, 0, 0, 0])
#         current_step = [1, 0, 0, 0]
#
#         while steps > 0.0:
#             current_step = self._get_next_counter(current_step)
#             self._gpio_setup(channels, current_step)
#             steps -= 1
#
#         self._gpio_setup(channels, [0, 0, 0, 0])
#
#
#     def _counter_turn(self, channels, steps):
#         # Turn the given motor left by a given number of degrees.
#         #steps = get_steps(deg)
#         self._gpio_setup(channels, [0, 0, 0, 0])
#         self._gpio_setup(channels, [1, 0, 0, 1])
#         current_step = [1, 0, 0, 1]
#
#         while steps > 0.0:
#             current_step = self._get_next_counter(current_step)
#             self._gpio_setup(channels, current_step)
#             steps -= 1
#
#         self._gpio_setup(channels, [0, 0, 0, 0])
#
#
#     def _get_next_clock(self, current_step):
#         # Big ugly function brute forcing the steps.  Find a better way!
#         if current_step == [1, 0, 0, 0]:
#             return [1, 1, 0, 0]
#         elif current_step == [1, 1, 0, 0]:
#             return [0, 1, 0, 0]
#         elif current_step == [0, 1, 0, 0]:
#             return [0, 1, 1, 0]
#         elif current_step == [0, 1, 1, 0]:
#             return [0, 0, 1, 0]
#         elif current_step == [0, 0, 1, 0]:
#             return [0, 0, 1, 1]
#         elif current_step == [0, 0, 1, 1]:
#             return [0, 0, 0, 1]
#         elif current_step == [0, 0, 0, 1]:
#             return [1, 0, 0, 1]
#         else: # current_step == [1, 0, 0, 1]
#             return [1, 0, 0, 0]
#
#     def _get_next_counter(self, current_step):
#         # Big ugly function brute forcing the steps.  Find a better way!
#         if current_step == [1, 0, 0, 1]:
#             return [0, 0, 0, 1]
#         elif current_step == [0, 0, 0, 1]:
#             return [0, 0, 1, 1]
#         elif current_step == [0, 0, 1, 1]:
#             return [0, 0, 1, 0]
#         elif current_step == [0, 0, 1, 0]:
#             return [0, 1, 1, 0]
#         elif current_step == [0, 1, 1, 0]:
#             return [0, 1, 0, 0]
#         elif current_step == [0, 1, 0, 0]:
#             return [1, 1, 0, 0]
#         elif current_step == [1, 1, 0, 0]:
#             return [1, 0, 0, 0]
#         else: # current_step == [1, 0, 0, 0]
#             return [1, 0, 0, 1]
#
#
# # -------------------------------------------------------------------------
#
#
# if __name__ == '__main__':
#
#     # Perform a few tests on the motors.
#     motor = CameraMotor({ 'x': 0.0, 'y': 0.0, 'z': 0.0 })
#     zero = motor.get_location()
#     for key, value in zero.items():
#         print(key + ": " + str(value))
#
#     motor.move({ 'x': 10.0, 'y': -10.0, 'z': 10.0 })
#
#     zero = motor.get_location()
#     for key, value in zero.items():
#         print(key + ": " + str(value))
#
#     print("done! :D")
#
#
#
#
#
# # -------------------------------------------------------------------------
