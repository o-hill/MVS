from intervals import Interval
import threading

# 5 seconds
stop_time = 10

# 1 image per second
interval = 2

# From the webcam
source = 0

Interval(stop_time, interval, source)
Interval(5, 1, 0)

print(threading.active_count())

print("done!")

