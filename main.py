from flask import Flask, render_template, Response, request,redirect,url_for
from camera import VideoCamera


app = Flask(__name__)
_red = 0
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route("/get_data", methods=["POST"])
def get_data():
    if request.method == "POST":
        red = request.form["red"]
        # green = request.form["green"]
        # blue = request.form["blue"]
        _red = red
        print(_red)
        return redirect(url_for('index'))


def gen(camera):
    # red,blue,green = get_data()
    while True:
        print(_red)
        frame = camera.get_frame(_red)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080, debug=True)
