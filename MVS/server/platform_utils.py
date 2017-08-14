from math import cos, sin, atan2, sqrt, pi
import time
import threading
import pylab as plt
import numpy as np


# --------------------------------------------------------------------------


class PlatformPosition(object):
    # Object that holds a position and recalculates
    # it's polar and cartesian position based on given input.

    def __init__(self):
        self.__dict__['x'] = 0
        self.__dict__['y'] = 0
        self.__dict__['r'] = 0
        self.__dict__['theta'] = 0
        self.__dict__['z'] = 0


    def __setattr__(self, name, value):
        # Set the x, y, r, or theta attributes of the class.
        # e.g. self.y += 2 -> calculates new polar coordinates.
        self.__dict__[name] = value

        if name == 'x' or name == 'y':
            self._calculate_polar()

        elif name == 'r' or name == 'theta':
            self._calculate_cartesian()


    def _calculate_polar(self):
        # Recalculates polar coordinates.
        self.__dict__['r'] = sqrt(self.x ** 2 + self.y ** 2)
        self.__dict__['theta'] = atan2(self.y, self.x)


    def _calculate_cartesian(self):
        # Recalculates cartesian coordinates.
        self.__dict__['x'] = self.r * cos(self.theta)
        self.__dict__['y'] = self.r * sin(self.theta)


    def update(self, polar_deltas):
        # Update the current coordinates.
        self.r += polar_deltas[0]
        self.theta += polar_deltas[1]
        self.z += polar_deltas[2]


    def go_home(self):
        self.x = 0
        self.y = 0


    def get_polar(self):
        # Return polar coordinates.
        return [self.r, self.theta, self.z]


    def get_cartesian(self):
        # Return cartesian coordinates.
        return [self.x, self.y, self.z]


    @property
    def polar(self):
        return self.get_polar()


    @property
    def cartesian(self):
        return self.get_cartesian()



# --------------------------------------------------------------------------



class PolarUtils(object):
    # Does the conversion math to return polar deltas,
    # given current position and cartesian deltas.


    def get_polar_delta(self, delta, position):
        # General move function for the motors.
        # DELTA: [dx, dy, dz].
        # POSITION: [r_curr, theta_curr, z_curr]

        delta_r = self.get_delta_r(delta, position)


        # Calculate delta_theta, using delta_r to model the
        # direction of the vector.
        r = position[0] + (1.25 * delta_r)
        one = -sin(position[1]) * delta[0]
        two = cos(position[1]) * delta[1]
        delta_theta = (one + two) / r

        print("delta theta: " + str(delta_theta))

        # Return the polar deltas.  We get dz for free!
        print("delta r: " + str(delta_r))
        return [delta_theta, delta_r, delta[2]]


    def get_delta_r(self, delta, position):
        # Calculate delta_r given cartesian deltas and current position.
        one = cos(position[1]) * delta[0]
        two = sin(position[1]) * delta[1]
        return one + two



# --------------------------------------------------------------------------


if __name__ == '__main__':

    # Create the Movement object.
    movement = Cords()

    # Define constant dx and dy.
    delta_x = 0.01
    delta_y = 0.01

    ideal_delta = 0.01
    ideal_num = 0.0

    # Create a tuple to pass to the movement object.
    delta = (delta_x, delta_y)

    trajectory = []
    ideal = []

    # Start at the origin.
    trajectory.append(movement.cartesian)
    ideal.append([ideal_num, ideal_num])


    for i in range (300):
        # Move the object to cartesian coordinates (3, 3)
        movement.move(delta)
        # Create a list of points the object visited.
        trajectory.append(movement.cartesian)
        # Create a list of the ideal path.
        ideal_num += ideal_delta
        ideal.append([ideal_num, ideal_num])


    # Create numpy arrays out of the coordinate lists.
    trajectory = np.array(trajectory)
    ideal = np.array(ideal)

    # Plot the lists.
    plt.close('all')
    plt.plot(trajectory[:, 0], trajectory[:, 1], label = 'polar')
    plt.plot(ideal[:, 0], ideal[:, 1], label = 'ideal')
    plt.legend()

    print("Final cartesian coordinates: " + str(movement.cartesian))





# --------------------------------------------------------------------------
