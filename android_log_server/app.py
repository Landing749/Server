from flask import Flask, request, render_template, redirect
import os
from datetime import datetime

app = Flask(__name__)

LOG_DIR = "user_logs"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route('/')
def index():
    return "Android Logger Server is Running."

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    device_id = data.get("device_id")
    log_data = data.get("log")

    if not device_id or not log_data:
        return {"status": "error", "message": "Missing device_id or log"}, 400

    user_folder = os.path.join(LOG_DIR, device_id)
    os.makedirs(user_folder, exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    filepath = os.path.join(user_folder, filename)

    with open(filepath, "w") as f:
        f.write(log_data)

    return {"status": "success"}

@app.route('/dashboard')
def dashboard_redirect():
    return redirect('/dashboard/input')

@app.route('/dashboard/input')
def dashboard_input():
    return '''
    <form action="/dashboard/view" method="get">
        <label>Enter Android ID:</label>
        <input type="text" name="device_id" />
        <input type="submit" value="View Logs" />
    </form>
    '''

@app.route('/dashboard/view')
def dashboard_view():
    device_id = request.args.get('device_id')
    log_folder = os.path.join(LOG_DIR, device_id)
    
    if not os.path.exists(log_folder):
        return f"<h2>No logs found for device ID: {device_id}</h2>"

    logs = []
    for filename in sorted(os.listdir(log_folder), reverse=True):
        with open(os.path.join(log_folder, filename)) as f:
            logs.append((filename, f.read()))

    return render_template("dashboard.html", device_id=device_id, logs=logs)
