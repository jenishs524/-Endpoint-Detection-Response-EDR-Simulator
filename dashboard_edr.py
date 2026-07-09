#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import threading
from edr_sim import alerts, alert_lock, monitor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('edr_dashboard.html')

@app.route('/api/alerts')
def get_alerts():
    with alert_lock:
        return jsonify(list(alerts))

if __name__ == "__main__":
    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
