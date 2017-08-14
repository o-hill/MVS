from motor import Motor
from cord_utility import Position


# -----------------------------------------------------------------------------


class Platform(object):
    # Models the physical platform of the device.
    # Controls the three onboard motors.

    def __init__(self):
        # Begins at the origin [0, 0, 0]
        self.motor = Motor()
        self.position = Position()


    def move(self, cart_delta):
        # Move given deltas!
        # TODO: Check to see if the delta crosses the forbidden boundary.

        # TODO: Move the motors iteratively, unthreaded.

        current = self.position.cartesian
        polar_deltas = self.utils.get_polar_delta(cart_delta, current)

        # Move the motors.
        self.motor.move(polar_deltas)
        # Update the current position.
        self.position.update(polar_deltas)


    def move_to(self, cords):
        # Move to a location!
        # Generate cartesian deltas.
        current = self.position.cartesian
        cart_delta = [
            cords[0] - current[0],
            cords[1] - current[1],
            cords[2] - current[2]
        ]

        # Move!
        self.move(cart_delta)


    def check_rotation(self, current, cart_deltas):
        # Check to see if the motors will cross the boundary
        # at pi.  If they will, redirect!
        future_x = current[0] + cart_deltas[0]
        future_y = current[1] + cart_deltas[1]
        future_z = current[2] + cart_deltas[2]

        print("future_x: " + str(future_x))
        print("future_y: " + str(future_y))
        print("future_z: " + str(future_z))

        print("current x: " + str(current[0]))
        print("current y: " + str(current[1]))
        print("current z: " + str(current[2]))

        slope = (future_y - current[1]) / (future_x - current[0])

        y_intercept = -(slope * current[0]) + current[1]
        x_intercept = y_intercept / slope

        print("slope: " + str(slope))
        print("y: " + str(y_intercept))
        print("check: " + str(x_intercept))

        if  x_intercept < 0:
            # Abort!  We can't cross the boundary between
            # quadrants II and III due to local mechanics.
            # Go to the (0, 0, 0) position (reset theta as well),
            # and continue from there.
            print("before")
            self.motor.platform_phone_home(current)
            self.position.go_home()
            self.move_to([future_x, future_y, future_z])
            print("after")
            return False

        return True

    @property
    def location(self):
        return self.position.cartesian





# --------------------------- TEST -----------------------------------------

if __name__ == '__main__':

    import pylab as plt
    plt.ion()

    plat = Platform()

    trajectory = []

    delta = [0.01, 0.01, 0]

    for num in range(300):
        plat.move(delta)
        trajectory.append(plat.location)

    trajectory = np.array(trajectory)
    plt.plot(trajectory[:, 0], trajectory[:, 1])

    # # Move to the second qudrant.
    # plat.move_to([-1, 1, 0])
    #
    # # Move to the third quadrant.  The motors
    # # should take us back to the origin first.
    # plat.move_to([-1, -1, 0])















# -----------------------------------------------------------------------------
