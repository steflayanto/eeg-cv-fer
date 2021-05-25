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

def render_home():
    eeg_b=("eeg_path" in session)
    cv_b = ("cv_path" in session)
    if ("label_frequency" in session):
        label_freq = session['label_frequency']
    else:
        label_freq = 1
        session['label_frequency'] = 1
    if ("eeg_model_name" in session):
        eeg_name = session['eeg_model_name']
    else:
        eeg_name = "defaulteeg"
        session['eeg_model_name'] = "defaulteeg"
    if ("cv_model_name" in session):
        cv_name = session['cv_model_name']
    else:
        cv_name = "defaultcv"
        session['cv_model_name'] = "defaultcv"
    return render_template('index.html',
                            eeg_valid = eeg_b,
                            cv_valid =  cv_b,
                            eeg_name = eeg_name,
                            cv_name = cv_name,
                            label_freq = label_freq)

@app.route('/')
def index():
    return render_home()

@app.route('/',methods=["POST"]) 
def upload_file():
    uploaded_file = request.files['file']
    if 'video' in uploaded_file.content_type:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))
        just_name = Path(uploaded_file.filename).stem
        subprocess.call([sys.executable, '../modelRunner.py', '-n', f'{session["cv_model_name"]}', '-d', f'uploads/{uploaded_file.filename}'])
        session["cv_path"] = f"./output/default-mtcnn-{just_name}.json"
        session["raw_video_path"] = "uploads/" + uploaded_file.filename
    elif "dat" in uploaded_file.filename:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))
        just_name = Path(uploaded_file.filename).stem
        subprocess.call([sys.executable, '../modelRunner.py', '-n', f'{session["eeg_model_name"]}', '-d', f'uploads/{uploaded_file.filename}'])
        session["eeg_path"] = f"./output/default-eeg-{just_name}.json"
    
    return render_home()

@app.route('/set_parameter', methods=["POST"]) 
def set_parameter():
    print(request.get_data())
    session['label_frequency'] = request.form['output_frequency']
    session['cv_model_name'] = request.form['cv-model']
    session['eeg_model_name'] = request.form['eeg-model']
    return render_home()

@app.route('/clear_session')
def clear():
    session.clear()
    return render_home()

@app.route('/run')
def run():
    if not "eeg_path" in session and not "cv_path" in session:
        return render_home()
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
        subprocess.call([sys.executable, '../modelRunner.py', '-n', 'joint', '-c', f'{session["cv_path"]}', '-e', f'{session["eeg_path"]}'])
        combined_data_path = f"./output/joint-{session['eeg_model_name']}-{session['cv_model_name']}.json"
        with open(combined_data_path) as fd:
            combined_data = json.load(fd)
            print(combined_data)
        return render_template('playback.html', eeg_data=json.dumps(eeg_data), cv_data=json.dumps(cv_data), video_path=session["raw_video_path"], combined_data=json.dumps(combined_data))

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory("./uploads/", filename)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
