from flask import Flask, request, render_template, session, send_from_directory
import subprocess
import sys
import numpy as np
import json
import os
from pathlib import Path


app = Flask(__name__, static_url_path='/uploads')
app.config.from_object(__name__)
app.secret_key = 'fake_secret'

# Generic function to render the index page, checking the session
# for values we may want to render the page with. Also sets default
# values in session.
def render_home():
    eeg_b=("raw_eeg_path" in session)
    cv_b = ("raw_video_path" in session)
    if ("label_frequency" in session):
        label_freq = session['label_frequency']
    else:
        label_freq = "1"
        session['label_frequency'] = "1"
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
    print(label_freq)
    return render_template('index.html',
                            eeg_valid = eeg_b,
                            cv_valid =  cv_b,
                            eeg_name = eeg_name,
                            cv_name = cv_name,
                            label_freq = label_freq)

# Index page
@app.route('/')
def index():
    return render_home()

# EEG classifier processing function. Calls the modelRunner script for EEG, and stores the classifier output
# in the session.
def process_eeg(eeg_path):
    subprocess.call([sys.executable, '../modelRunner.py', '-l', f'{session["label_frequency"]}', '-n', f'{session["eeg_model_name"]}', '-d', f'{eeg_path}'])
    subprocess.call([sys.executable, '../modelRunner.py', '-l', f'{session["label_frequency"]}', '-n', 'defaulteegpower', '-d', f'{eeg_path}'])
    session["eeg_path"] = f"./{session['eeg_model_name']}.json"
    session["eeg_power_path"] = "./defaulteegpower.json"

# CV classifier processing function. Calls the modelRunner script for CV, and stores the classifier output
# in the session.
def process_cv(cv_path):
    subprocess.call([sys.executable, '../modelRunner.py', '-l', f'{session["label_frequency"]}', '-n', f'{session["cv_model_name"]}', '-d', f'{cv_path}'])
    session["cv_path"] = f"./{session['cv_model_name']}.json"

# Generic POST handling on the index page.
@app.route('/',methods=["POST"]) 
def upload_file():
    uploaded_file = request.files['file']
    if 'video' in uploaded_file.content_type:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))
        session["raw_video_path"] = "uploads/" + uploaded_file.filename

    elif "dat" in uploaded_file.filename:
        uploaded_file.save(os.path.join("uploads/", uploaded_file.filename))
        session["raw_eeg_path"] = "uploads/" + uploaded_file.filename

    return render_home()

# Handles the set_parameter fields from the index page. Updates session values.
@app.route('/set_parameter', methods=["POST"]) 
def set_parameter():
    print(request.get_data())
    session['label_frequency'] = request.form['output_frequency']
    session['cv_model_name'] = request.form['cv-model']
    session['eeg_model_name'] = request.form['eeg-model']
    return render_home()

# Clears the session of any previously stored values.
@app.route('/clear_session')
def clear():
    session.clear()
    return render_home()

# Runs the classifiers, calling process_eeg and process_cv, and then rendering the final output page
# where we display the data to the user.
@app.route('/run')
def run():
    playback_interval_ms = (1.0 / float(session["label_frequency"])) * 1000.0
    if not "raw_eeg_path" in session and not "raw_video_path" in session:
        return render_home()
    elif not "raw_eeg_path" in session:
        process_cv(session['raw_video_path'])
        cv_data = ""
        with open(session["cv_path"]) as fd:
            cv_data = json.load(fd)
            print(cv_data)
        return render_template('cvplayback.html',
                                cv_data=json.dumps(cv_data),
                                video_path=session["raw_video_path"],
                                playback_interval_ms=playback_interval_ms)
    elif not "raw_video_path" in session:
        process_eeg(session['raw_eeg_path'])
        eeg_data = ""
        with open(session["eeg_path"]) as fd:
            eeg_data = json.load(fd)
            print(eeg_data)
        with open(session["eeg_power_path"]) as fd:
            eeg_power_data = json.load(fd)
            print(eeg_power_data)
        return render_template('eegplayback.html',
                                eeg_data=json.dumps(eeg_data),
                                eeg_power_data=json.dumps(eeg_power_data),
                                playback_interval_ms=playback_interval_ms)
    else:
        process_cv(session['raw_video_path'])
        process_eeg(session['raw_eeg_path'])
        cv_data = ""
        eeg_data = ""
        with open(session["cv_path"]) as fd:
            cv_data = json.load(fd)
            print(cv_data)
        with open(session["eeg_path"]) as fd:
            eeg_data = json.load(fd)
            print(eeg_data)
        subprocess.call([sys.executable, '../modelRunner.py', '-n', 'dual', '-c', f'{session["cv_path"]}', '-e', f'{session["eeg_path"]}'])
        combined_data_path = f"./dual-{session['eeg_model_name']}-{session['cv_model_name']}.json"
        with open(combined_data_path) as fd:
            combined_data = json.load(fd)
            print(combined_data)
        return render_template('playback.html',
                                eeg_data=json.dumps(eeg_data),
                                cv_data=json.dumps(cv_data),
                                video_path=session["raw_video_path"],
                                combined_data=json.dumps(combined_data),
                                playback_interval_ms=playback_interval_ms)

# Handles requested video files from the user.
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory("./uploads/", filename)

# Main
if __name__ == '__main__':
    app.run(port = 5000, debug=True)
