from flask import Flask, render_template, Response, request,redirect,url_for
from camera import VideoCamera


app = Flask(__name__)
_red = 0
_green = 0
_blue = 0
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route("/get_data", methods=["POST"])
def get_data():
    global _red,_green,_blue
    if request.method == "POST":
        red = int(request.form["red"])
        green = int(request.form["green"])
        blue = int(request.form["blue"])
        _red = red
        _blue = blue
        _green = green
        return redirect(url_for('index'))


def gen(camera):
    while True:
        frame = camera.get_frame(_red,_blue,_green)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080, debug=True)
