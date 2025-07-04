from flask import Flask, render_template, request, redirect, jsonify, Response
from datetime import datetime
import requests
import hashlib
import os

app = Flask(__name__)
start_time = datetime.now()

GITHUB_APPROVAL_URL = "https://github.com/Serverx0/Darkstr/blob/main/Aprooval.txt"
KEY_FILE = "fingerprint.key"

def generate_or_load_fingerprint_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()

    fake_fingerprint = os.uname().nodename.encode()
    key = hashlib.sha256(fake_fingerprint).hexdigest()
    with open(KEY_FILE, "w") as f:
        f.write(key)
    return key

def is_approved():
    key = generate_or_load_fingerprint_key()
    try:
        response = requests.get(GITHUB_APPROVAL_URL)
        return response.status_code == 200 and key in response.text
    except:
        return False

@app.route('/')
def index():
    if not is_approved():
        return redirect("/approval")

    uptime = str(datetime.now() - start_time).split('.')[0]
    return render_template("index.html", servers=servers, start_time=int(start_time.timestamp() * 1000), uptime=uptime)

@app.route('/approval')
def approval():
    key = generate_or_load_fingerprint_key()
    return render_template("approval.html", device_key=key)

@app.route('/fingerprint', methods=["POST"])
def fingerprint():
    key = generate_or_load_fingerprint_key()
    try:
        response = requests.get(GITHUB_APPROVAL_URL)
        approved = response.status_code == 200 and key in response.text
    except:
        approved = False
    return jsonify({"approved": approved, "key": key})

@app.route("/open/<int:server_id>")
def open_tool(server_id):
    server = next((s for s in servers if s["id"] == server_id), None)
    if not server or server["url"] == "UPCOMING":
        return "Server not found", 404
    return render_template("open_tool.html", title=server["name"], tool_url=server["url"])

servers = [
    {
        "id": 1,
        "name": "WhatsApp Session Generator",
        "url": "http://fi9.bot-hosting.net:20277/",
        "image": "https://imagesaver.darkester.online/uploads/1751638854-1000012086.jpg"
    },
    {
        "id": 2,
        "name": "Convo Server",
        "url": "http://fi9.bot-hosting.net:20947/",
        "image": "https://imagesaver.darkester.online/uploads/1751638854-1000012086.jpg"
    },
    {
        "id": 3,
        "name": "Token Checker",
        "url": "http://fi5.bot-hosting.net:20136/",
        "image": "https://imagesaver.darkester.online/uploads/1751638854-1000012086.jpg"
    },
    {
        "id": 4,
        "name": "Backup Convo",
        "url": "http://de1.bot-hosting.net:22787/",
        "image": "https://imagesaver.darkester.online/uploads/1751638854-1000012086.jpg"
    },
    {
        "id": 5,
        "name": "WhatsApp Server",
        "url": "http://fi9.bot-hosting.net:21171/",
        "image": "https://imagesaver.darkester.online/uploads/1751638854-1000012086.jpg"
    },
    {
        "id": 6,
        "name": "Cookies To Token",
        "url": "https://generator.darkester.online/",
        "image": "https://imagesaver.darkester.online/uploads/1751638854-1000012086.jpg"
    },
   
]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
