from flask import Flask
from web_app.ui import root

app = Flask(__name__,template_folder="web_app/templates")
app.register_blueprint(root)
app.run(host="0.0.0.0")