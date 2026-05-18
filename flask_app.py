from flask import Flask, jsonify, render_template
from tester.runner import run_all
from storage import save_run, list_runs
from datetime import datetime

app = Flask(__name__)
application = app  # requis pour PythonAnywhere
API_NAME = "Frankfurter"

@app.route("/")
def index():
    return render_template("dashboard.html", runs=list_runs())

@app.route("/run")
def run():
    summary, tests = run_all()
    save_run(API_NAME, summary, tests)
    return jsonify({
        "api": API_NAME,
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "tests": tests
    })

@app.route("/dashboard")
def dashboard():
    runs = list_runs()
    return render_template("dashboard.html", runs=runs)

@app.route("/health")
def health():
    runs = list_runs(limit=1)
    last = runs[0] if runs else None
    return jsonify({
        "status": "ok",
        "last_run": last["timestamp"] if last else None,
        "last_summary": last["summary"] if last else None
    })

if __name__ == "__main__":
    app.run(debug=True)
