from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import os
import json
from datetime import datetime
import html
import uuid
import re
import random

app = Flask(__name__)

# File to store snippets
SNIPPET_FILE = "snippets.json"

# Directory to store uploaded files
FILE_DIRECTORY = "files"

# Banner file
BANNER_FILE = "banner.txt"

# In-memory storage for snippets
snippets = {}

# Ensure the file directory exists
if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)

# Load banners from file
def load_banners():
    if os.path.exists(BANNER_FILE):
        try:
            with open(BANNER_FILE, 'r', encoding='utf-8') as f:  # Specify UTF-8 encoding
                banners = f.read().strip().split("\n---\n")  # Split banners by "---"
            return [banner.strip() for banner in banners if banner.strip()]
        except UnicodeDecodeError as e:
            print(f"Error reading {BANNER_FILE}: {e}")
            return ["Error: Could not decode banners. Check the file encoding."]
    else:
        return ["LANBin"]  # Default banner if no file is found

# Select a random banner
def get_random_banner():
    banners = load_banners()
    return random.choice(banners)

# Load snippets from file
def load_snippets():
    global snippets
    if os.path.exists(SNIPPET_FILE):
        try:
            with open(SNIPPET_FILE, 'r') as f:
                snippets = json.load(f)
        except json.JSONDecodeError:
            print("Warning: `snippets.json` is invalid. Starting with an empty dictionary.")
            snippets = {}
    else:
        snippets = {}

# Save snippets to file
def save_snippets():
    with open(SNIPPET_FILE, 'w') as f:
        json.dump(snippets, f)

# Sanitize input and escape HTML characters
def sanitize_input(content):
    return html.escape(content)

# Detect URLs and wrap them in <a> tags
def make_links_clickable(content):
    url_pattern = r'(https?://[^\s]+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', content)

# Home Page
@app.route('/')
def home():
    files = os.listdir(FILE_DIRECTORY)  # List files in the directory
    return render_template('home.html', snippets=snippets, files=files)

# Create a new snippet
@app.route('/paste', methods=['POST'])
def paste():
    content = request.form.get('content')
    if not content:
        return jsonify({"error": "No content provided"}), 400

    # Generate a unique ID for the snippet
    snippet_id = str(uuid.uuid4())
    
    # Sanitize content
    sanitized_content = sanitize_input(content)

    # Add metadata to the snippet
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr

    # Store snippet with metadata
    snippets[snippet_id] = {
        "content": make_links_clickable(sanitized_content),
        "timestamp": timestamp,
        "ip": ip_address
    }

    # Save the snippets to disk
    save_snippets()

    # Redirect back to the home page
    return redirect(url_for('home'))

# Handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the files directory
    file.save(os.path.join(FILE_DIRECTORY, file.filename))

    # Redirect back to the home page
    return redirect(url_for('home'))

# Serve files for download
@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(FILE_DIRECTORY, filename)

# Delete a snippet
@app.route('/delete/<snippet_id>', methods=['POST'])
def delete_snippet(snippet_id):
    if snippet_id in snippets:
        del snippets[snippet_id]
        save_snippets()
        return redirect(url_for('home'))
    return jsonify({"error": "Snippet not found"}), 404

# Delete a file
@app.route('/delete_file/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(FILE_DIRECTORY, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('home'))
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    banner = get_random_banner()
    print(banner)
    print("\ngithub.com/deekaph/lanbin\n")  # Add GitHub link below the banner
    load_snippets()  # Load snippets from file
    app.run(host='0.0.0.0', port=5000)
