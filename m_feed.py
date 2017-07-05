from flask import Flask, Response, render_template
from camera import Camera
from gevent.wsgi import WSGIServer


app = Flask(__name__)

# Currently nothing - html document can be updated if needed.
@app.route("/")
def main():
	return render_template('homepage.html')

# Generator function to render jpeg frames from the camera.
def gen(camera):
	while True:
		frame = camera.get_image()
		yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Currently hardcoded to the second camera attached to the system
@app.route('/microscope_feed')
def microscope_feed():
	stream = Camera(1)
	generate = gen(stream)
	return Response(generate, mimetype='multipart/x-mixed-replace; boundary=frame')

# Start the application.
if __name__ == "__main__":
	port_number = 1493

	# Start the server
	http_server = WSGIServer(('', port_number), app)
	http_server.serve_forever()
