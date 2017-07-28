import time
import RPi.GPIO as GPIO # Raspberry Pi I/O library
import threading
from math import tan, sqrt # For polar conversion.

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(false)


# CURRENTLY:
#   Motor 1 is set up as R.
#   Motor 2 is set up as Theta.
#   Motor 3 is set up as Z.
#   R is defined by the number of steps to get there on the stepper motor.


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



class CameraMotors(threading.Thread):
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


    def move(self, coords):
        # Check to see if we need to move individual axes.
        # If we do, move them!
        threads = []
        polar = self._convert_to_polar(coords)

        if polar['r'] != self.current['r']:
            channels = get_channels(1)
            dest = polar['r'] - self.current['r']
            if polar['r'] < self.current['r']:
                # Spin the motor so it moves towards the center.
                direct = 'clock'
            else:
                # Otherwise, spin it so it moves toward the outer edge.
                direct = 'counter'
            # Designate a worker thread to handle the move.
            worker = threading.Thread(target=run, args(dest, channels, direct))
            threads.append(worker)

        if polar['theta'] != self.current['theta']:
            channels = get_channels(2)
            dest = polar['theta'] - self.current['theta']
            if polar['theta'] < self.current['theta']:
                direct = 'clock'
            else:
                direct = 'counter'
            worker = threading.Thread(target=run, args(dest, channels, direct))
            threads.append(worker)

        if polar['z'] != self.current['z']:
            channels = get_channels(3)
            dest = polar['z'] - self.current['z']
            if polar['z'] < self.current['z']:
                direct = 'clock'
            else:
                direct = 'counter'
            worker = threading.Thread(target=run, args(dest, channels, direct))
            threads.append(worker)

        # Start all of the worker threads.
        for worker in threads:
            worker.start()

        # Wait for all of the worker threads to finish their tasks.
        for worker in threads:
            worker.join()
            
        # Success! We moved!
        self.current = polar

    def get_channels(self, motor):
        # Return the appropriate control channels
        # based on which motor is specified.
        if motor == 1:
            return [7, 11, 13, 15]
        elif motor == 2:
            return [12, 16, 18, 22]
        else: # Motor 3.
            return [29, 31, 33, 35]


    def run(self, degree, channels, direction):
        if direction == 'clock':
            clockwise_turn()



    # Amount of steps in the motors circle.
    FULL_CIRCLE = 510.0

    def get_steps(deg):
        # Return the amount of steps required to
        # turn the given amount of degrees.
        return (FULL_CIRCLE/360) * deg

    #     Pin 1   Pin 2   Pin 3   Pin 4
    #  1    x
    #  2    x       x
    #  3            x
    #  4            x       x
    #  5                    x
    #  6                    x      x
    #  7                           x
    #  8    x                      x


    def gpio_setup(channels, inputs):
        # Loop through the two lists simultaneously,
        # and apply the motor changes to each channel.
        for chan, deg in zip(channels, inputs):
            GPIO.output(chan, deg)
        # Allow motor to catch up?
        time.sleep(0.001)


    def clockwise_turn(channels, deg):
        # Turn the given motor right by a given number of degrees.
        steps = get_steps(deg)
        gpio_setup(channels, [0, 0, 0, 0])

        while steps > 0.0:
            gpio_setup(channels, [1, 0, 0, 0])
            gpio_setup(channels, [1, 1, 0, 0])
            gpio_setup(channels, [0, 1, 0, 0])
            gpio_setup(channels, [0, 1, 1, 0])
            gpio_setup(channels, [0, 0, 1, 0])
            gpio_setup(channels, [0, 0, 1, 1])
            gpio_setup(channels, [0, 0, 0, 1])
            gpio_setup(channels, [1, 0, 0, 1])
            degree -= 1


    def counterclock_turn(channels, deg):
        # Turn the given motor left by a given number of degrees.
        steps = get_steps(deg)
        gpio_setup(channels, [0, 0, 0, 0])

        while steps > 0.0:
            gpio_setup(channels, [1, 0, 0, 1])
            gpio_setup(channels, [0, 0, 0, 1])
            gpio_setup(channels, [0, 0, 1, 1])
            gpio_setup(channels, [0, 0, 1, 0])
            gpio_setup(channels, [0, 1, 1, 0])
            gpio_setup(channels, [0, 1, 0, 0])
            gpio_setup(channels, [1, 1, 0, 0])
            gpio_setup(channels, [1, 0, 0, 0])
            degree -= 1


# -------------------------------------------------------------------------


if __name__ == '__main__':

    # Perform a few tests on the motors.






# -------------------------------------------------------------------------
