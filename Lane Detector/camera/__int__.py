import flask
from flask import Response
import os

from camera.camera import gen_localhttp_res

camera_blueprint = flask.Blueprint('camera_blueprint', __name__, url_prefix='/camera') #creates flask blueprint for camera components to be registered with flask app

@camera_blueprint.route('/stream')
def camera_stream():
    return Response(gen_localhttp_res(),mimetype='multipart/x-mixed-replace; boundary=frame')#utilizes opencv (usually webcam or first connected camera device) frame generator
        
