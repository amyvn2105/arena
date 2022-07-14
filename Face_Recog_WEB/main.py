from flask import Flask, Response
from app import views, utils
from prepare import *

app = Flask(__name__)

app.add_url_rule('/base','base',views.base)
app.add_url_rule('/','index',views.index)
app.add_url_rule('/faceapp','faceapp',views.faceapp)
app.add_url_rule('/faceapp/face_recog','face_recog',views.face_recog,methods=['GET','POST'])
@app.route('/video_feed')
def video_feed():
    return Response(utils.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)