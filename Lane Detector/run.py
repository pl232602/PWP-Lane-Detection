from flask import Flask
from camera_provider import camera_blueprint
from ui import root

app = Flask(__name__)
app.register_blueprint(root)
app.register_blueprint(camera_blueprint)
app.run(host="0.0.0.0")