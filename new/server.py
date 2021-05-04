from flask import Flask, request,render_template
import numpy as np
import json
import os


app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods=["POST"])
def upload_file():
    uploaded_file = request.files['image']
    if 'mp4' in uploaded_file.filename:
        uploaded_file.save(os.path.join("static/",uploaded_file.filename))
        return render_template('index.html', video_path=os.path.join("static/",uploaded_file.filename))
    if "npy" in uploaded_file.filename:
        print("hi")
    
    
    uploaded_file.save(os.path.join("uploads/",uploaded_file.filename))
    return render_template('index.html')

@app.route('/',methods=["GET"])
def get():
    return send_file(os.path.join("uploads/",uploaded_file.filename))

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
