from flask import Flask, request, render_template
from collections import defaultdict

app = Flask(__name__)

# Store logs per android_id in memory (temporary)
logs = defaultdict(list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard/<android_id>')
def dashboard(android_id):
    user_logs = logs.get(android_id, [])
    return render_template('dashboard.html', android_id=android_id, logs=user_logs)

@app.route('/log', methods=['POST'])
def log():
    android_id = request.form.get('android_id')
    text = request.form.get('text')

    if android_id and text:
        logs[android_id].append(text)
        return "Log received", 200
    return "Missing fields", 400

if __name__ == "__main__":
    app.run(debug=True)
