from flask import Flask
from ui import root

app = Flask(__name__)
app.register_blueprint(root)