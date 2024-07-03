from flask import Flask, request, send_from_directory
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'test.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.get_json()
    command = data.get('command')
    
    try:
        os.environ['DISPLAY'] = ':0'

        process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return stdout
        else:
            return stderr, 400
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
