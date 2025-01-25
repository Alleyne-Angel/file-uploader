from flask import Flask, request, send_from_directory, jsonify
import os
from yaml import safe_load

app = Flask(__name__)

# define the path to save
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
with open('./config.yaml') as file:
    token = safe_load(file)['token']

# The route to upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.headers.get('token') != '':
        return jsonify({"error": "Invalid token"}), 403
    # check file tag
    if 'file' not in request.files:
        return jsonify({"error": "No file part detected"}), 400 
    file = request.files['file']
    
    # if no file
    if not file.filename:
        return jsonify({"error": "No selected file"}), 400
    
    # save file
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filePath)
    
    return jsonify({"message": "File uploaded successfully", "file_path": filePath}), 200


# The route to retrieve file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # send file
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404