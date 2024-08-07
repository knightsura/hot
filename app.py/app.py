from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory storage for images and votes
images = []
votes = {}

@app.route('/')
def index():
    return render_template('index.html', images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            images.append(filename)
            votes[filename] = 0
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/vote/<filename>', methods=['POST'])
def vote(filename):
    if filename in votes:
        votes[filename] += 1
    return redirect(url_for('index'))

@app.route('/results')
def results():
    sorted_images = sorted(images, key=lambda img: votes[img], reverse=True)
    return render_template('results.html', images=sorted_images, votes=votes)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
