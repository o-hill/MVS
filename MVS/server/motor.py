import time
import RPi.GPIO as GPIO # Raspberry Pi I/O library
import threading
from math import cos, sin, tan, sqrt # For polar conversion.


# CURRENTLY ASSUMING:
#   Motor 1 is set up as R.
#   Motor 2 is set up as Theta.
#   Motor 3 is set up as Z.
#   R is defined by the number of steps to get there on the stepper motor.
#   Clockwise rotation always results in a move towards (0, 0, 0)


    # # Motor 1.
    # motor_1_channels =
    # GPIO.setup(motor_1_channels, GPIO.OUT)
    #
    # # Motor 2.
    # # Will most likely be changed - port 12 will be used for light dimmer.
    # motor_2_channels =
    # GPIO.setup(motor_2_channels, GPIO.OUT)
    #
    # # Motor 3.
    # motor_3_channels =
    # GPIO.setup(motor_3_channels, GPIO.OUT)



class CameraMotor():
    # A multithreaded component that operates
    # stepper motors to control the camera.
    # Given the rectangular coordinates of where to move,
    # the class will be able to get there.

    # def __init__(self, degree, motor, direction):
    #     # Inputs:
    #     #   degree: integer that describes how far to turn the motor.
    #     #   motor: integer that describes which motor to turn.
    #     #   direction: string, either 'clock' or 'counterclock'.
    #     channels = get_channels(motor)
    #     GPIO.setup(channels, GPIO.OUT)
    #     self.start(degree, channels, direction)

    def __init__(self, current_coords):
        # current_coords: a dictionary of three recatangular
        # coordinates describing where the camera is currently.
        self.current = self._convert_to_polar(current_coords)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(false)

        # Amount of steps in the motors circle.
        self.FULL_CIRCLE = 510.0


    def _convert_to_polar(self, coords):
        new_coords = {}
        # Get R in polar.
        x_square = coords['x'] ** 2
        y_square = coords['y'] ** 2
        new_coords['r'] = sqrt(x_square + y_square)
        # Get theta in polar.
        new_coords['theta'] = 1 / (tan(coords['y'] / coords['x']))
        # We get Z for free!
        new_coords['z'] = coords['z']
        return new_coords


    def _convert_to_cartesian(self, coords):
        new_coords = {}
        polar = self.current
        new_coords['x'] = polar['r'] * cos(polar['theta'])
        new_coords['y'] = polar['r'] * sin(polar['theta'])
        new_coords['z'] = polar['z']
        return new_cords


    def move(self, coords):
        threads = []
        polar = self._convert_to_polar(coords)

        motor = 1
        for cord, pos in self._current.items():
            # Get worker threads for which ever motors
            # need to be moved to get to the next position.
            if polar[cord] != self.current[cord]:
                worker = self._get_worker(cord, polar, motor)
                threads.append(worker)
            motor += 1

        # Start all of the worker threads.
        for worker in threads:
            worker.start()

        # Wait for all of the worker threads to finish their tasks.
        for worker in threads:
            worker.join()

        # Success! We moved!  Signal that we are done.
        self.current = polar
        return 1


    def _get_worker(self, cord, polar, motor):
        # Cord: a string containing either 'r', 'theta', or 'z'.
        # Polar: a dictionary containing the three coordinates.
        # Motor: an int describing which set of Pi channels to use.
        #   Either 1, 2, or 3.
        channels = get_channels(motor)
        dest = polar[cord] - self.current[cord]
        if cord == 'r' or cord == 'z':
            if polar[cord] < self.current[cord]:
                # Spin the motor so it moves towards (0, 0, 0).
                direct = 'clock'
            else:
                # Otherwise, spin it so it moves away from the origin.
                direct = 'counter'
        else: # cord == 'theta'
            distance = polar[cord] - self.current[cord]
            if distance < 180: # Move clockwise.
                direct = 'clock'
            else: # Move counter clockwise.
                direct = 'counter'

        # Designate a worker thread to handle the move.
        worker = threading.Thread(target=self._run, args(dest, channels, direct))
        return worker


    def get_channels(self, motor):
        # Return the appropriate control channels
        # based on which motor is specified.
        if motor == 1:
            return [7, 11, 13, 15]
        elif motor == 2:
            return [12, 16, 18, 22]
        else: # Motor 3.
            return [29, 31, 33, 35]


    def _run(self, num_steps, channels, direction):
        if direction == 'clock':
            self._clockwise_turn(channels, num_steps)
        else: # direction == 'counter'
            self._counter_turn(channels, num_steps)


    def get_location(self):
        return self._convert_to_cartesian(self.current)


    def _get_steps(deg):
        # Return the amount of steps required to
        # turn the given amount of degrees.
        return (self.FULL_CIRCLE/360) * deg

    #     Pin 1   Pin 2   Pin 3   Pin 4
    #  1    x
    #  2    x       x
    #  3            x
    #  4            x       x
    #  5                    x
    #  6                    x      x
    #  7                           x
    #  8    x                      x


    def _gpio_setup(channels, inputs):
        # Loop through the two lists simultaneously,
        # and apply the motor changes to each channel.
        for chan, step in zip(channels, inputs):
            GPIO.output(chan, step)
        # Allow motor to catch up?
        time.sleep(0.001)


    def _clockwise_turn(channels, steps):
        # Turn the given motor right by a given number of degrees.
        #steps = get_steps(deg)
        _gpio_setup(channels, [0, 0, 0, 0])
        _gpio_setup(channels, [1, 0, 0, 0])
        current_step = [1, 0, 0, 0]

        while steps > 0:
            current_step = _get_next_counter(current_step)
            _gpio_setup(channels, current_step)
            step -= 1

        # while steps > 0.0:
        #     gpio_setup(channels, [1, 0, 0, 0])
        #     gpio_setup(channels, [1, 1, 0, 0])
        #     gpio_setup(channels, [0, 1, 0, 0])
        #     gpio_setup(channels, [0, 1, 1, 0])
        #     gpio_setup(channels, [0, 0, 1, 0])
        #     gpio_setup(channels, [0, 0, 1, 1])
        #     gpio_setup(channels, [0, 0, 0, 1])
        #     gpio_setup(channels, [1, 0, 0, 1])
        #     degree -= 1


    def _counter_turn(channels, steps):
        # Turn the given motor left by a given number of degrees.
        #steps = get_steps(deg)
        _gpio_setup(channels, [0, 0, 0, 0])
        _gpio_setup(channels, [1, 0, 0, 1])
        current_step = [1, 0, 0, 1]

        while steps > 0:
            current_step = _get_next_counter(current_step)
            _gpio_setup(channels, current_step)
            step -= 1

        # while steps > 0.0:
        #     gpio_setup(channels, [1, 0, 0, 1])
        #     gpio_setup(channels, [0, 0, 0, 1])
        #     gpio_setup(channels, [0, 0, 1, 1])
        #     gpio_setup(channels, [0, 0, 1, 0])
        #     gpio_setup(channels, [0, 1, 1, 0])
        #     gpio_setup(channels, [0, 1, 0, 0])
        #     gpio_setup(channels, [1, 1, 0, 0])
        #     gpio_setup(channels, [1, 0, 0, 0])
        #     degree -= 1


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


# -------------------------------------------------------------------------


if __name__ == '__main__':

    # Perform a few tests on the motors.
    motor = CameraMotor({ 'x': 0, 'y': 0, 'z': 0 })

    zero = motor.get_location()
    for key, value in zero.items():
        print(key + ": " + str(value))

    motor.move({ 'x': 700, 'y': 700, 'z': 300 })

    zero = motor.get_location()
    for key, value in zero.items():
        print(key + ": " + str(value))





# -------------------------------------------------------------------------
