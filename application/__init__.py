from flask import Flask
from flask_session import Session
import os
from flask_cors import CORS



app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SECRET_KEY"] ='449bf441804501016c9fdcc8c2684a347dda16f7d359c39d6374df211f42'
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)
dir_path = os.path.dirname(os.path.realpath(__file__))
app.config.update(
    UPLOADED_PATH = os.path.join(dir_path, "static/uploaded_files/"),
    AUDIO_FILE_UPLOAD = os.path.join(dir_path, 'static/audio_files/')
)

from application import routes
