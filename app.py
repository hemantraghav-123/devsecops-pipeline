from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "DevSecOps Pipeline - Hemant Raghav",
        "version": "3.0",
        "time": str(datetime.datetime.now())
    })

@app.route('/health')
def health():
    return jsonify({"health": "OK"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
