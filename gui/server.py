from flask import Flask, request,render_template, session
from flask_session import Session
import numpy as np
import json
import os
import ffmpeg

app = Flask(__name__, static_url_path='/uploads')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def index():
    return render_template('index.html', eeg_valid=("eeg_path" in session), cv_valid = ("cv_path" in session))

@app.route('/',methods=["POST"])
def upload_file():
    uploaded_file = request.files['image']
    if 'video' in uploaded_file.content_type:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))

        # ffmpeg conversion
        #stream = ffmpeg.input("uploads/" + uploaded_file.filename)
        #new_filename = os.path.splitext(uploaded_file.filename)[0] + ".mp4"
        #stream = ffmpeg.output(stream, new_filename)
        #ffmpeg.run(stream)

        session["cv_path"] = uploaded_file.filename
        session["raw_video_path"] = "uploads/" + uploaded_file.filename
    elif "npy" in uploaded_file.filename:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))
        session["eeg_path"] = "uploads/" + uploaded_file.filename
    
    uploaded_file.save(os.path.join("uploads/",uploaded_file.filename))
    return render_template('index.html', eeg_valid=("eeg_path" in session), cv_valid = ("cv_path" in session))


@app.route('/run')
def run():
    if not "eeg_path" in session and not "cv_path" in session:
        return render_template('index.html', eeg_valid=("eeg_path" in session), cv_valid = ("cv_path" in session))
    elif not "eeg_path" in session:
        return render_template('cvplayback.html', cv_path=session["cv_path"], video_path=session["raw_video_path"])
    elif not "cv_path" in session:
        return render_template('eegplayback.html', eeg_path=session["eeg_path"])
    else:
        return render_template('playback.html', eeg_path=session["eeg_path"], cv_path=session["cv_path"], video_path=session["raw_video_path"])

@app.route('/',methods=["GET"])
def get():
    return send_file(os.path.join("uploads/",uploaded_file.filename))

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
