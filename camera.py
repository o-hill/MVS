import cv2
import time
from imutils.video import VideoStream

class Camera:

	def __init__(self, src = 0):
		self.stream = cv2.VideoCapture(src)
		time.sleep(2)
		self.frame = self.stream.read()


	def get_image(self):
		_, frame = self.stream.read()
		ret, jpeg = cv2.imencode(".jpg", frame)
		return jpeg.tobytes()


	def __del__(self):
		del(self.stream)
	
