from flask import Flask, request, render_template, session, send_from_directory
from flask_session import Session
import subprocess
import sys
import numpy as np
import json
import os
from pathlib import Path

app = Flask(__name__, static_url_path='/uploads')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def index():
    return render_template('index.html', eeg_valid=("eeg_path" in session), cv_valid = ("cv_path" in session))

@app.route('/',methods=["POST"])
def upload_file():
    uploaded_file = request.files['file']
    if 'video' in uploaded_file.content_type:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))
        just_name = Path(uploaded_file.filename).stem
        subprocess.call([sys.executable, '../modelRunner.py', '-n', 'defaultcv', '-d', f'uploads/{uploaded_file.filename}'])
        session["cv_path"] = f"./output/default-mtcnn-{just_name}.json"
        session["raw_video_path"] = "uploads/" + uploaded_file.filename
    elif "npy" in uploaded_file.filename:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))
        just_name = Path(uploaded_file.filename).stem
        subprocess.call([sys.executable, '../modelRunner.py', '-n', 'defaulteeg', '-d', f'uploads/{uploaded_file.filename}'])
        session["eeg_path"] = f"./output/default-eeg-{just_name}.json"
    
    return render_template('index.html', eeg_valid=("eeg_path" in session), cv_valid = ("cv_path" in session))

@app.route('/run')
def run():
    if not "eeg_path" in session and not "cv_path" in session:
        return render_template('index.html', eeg_valid = ("eeg_path" in session), cv_valid = ("cv_path" in session))
    elif not "eeg_path" in session:
        cv_data = ""
        with open(session["cv_path"]) as fd:
            cv_data = json.load(fd)
            print(cv_data)
        return render_template('cvplayback.html', cv_data=json.dumps(cv_data), video_path=session["raw_video_path"])
    elif not "cv_path" in session:
        eeg_data = ""
        with open(session["eeg_path"]) as fd:
            eeg_data = json.load(fd)
            print(eeg_data)
        return render_template('eegplayback.html', eeg_data=json.dumps(eeg_data))
    else:
        cv_data = ""
        eeg_data = ""
        with open(session["cv_path"]) as fd:
            cv_data = json.load(fd)
            print(cv_data)
        with open(session["eeg_path"]) as fd:
            eeg_data = json.load(fd)
            print(eeg_data)
        return render_template('playback.html', eeg_data=json.dumps(eeg_data), cv_data=json.dumps(cv_data), video_path=session["raw_video_path"])

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory("./uploads/", filename)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
