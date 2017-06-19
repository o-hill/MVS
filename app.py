from flask import Flask, Response, render_template
from camera import Camera


app = Flask(__name__)

@app.route("/")
def main():
	return render_template('homepage.html')

def gen(camera):
	while True:
		frame = camera.get_image()
		yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
	stream = Camera()
	generate = gen(stream)
	return Response(generate, mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True)
