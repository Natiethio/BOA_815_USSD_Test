from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import subprocess, os


app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-test', methods=['POST'])
def run_test():
    data = request.get_json()
    device_id       = data.get('device_id', '').strip()
    android_ver     = data.get('android_version', '').strip()
    account_number  = data.get('account_number', '').strip()
    pin             = data.get('pin', '').strip()
    amount          = data.get('amount', '').strip()
    phone_number    = data.get('phone_number', '').strip()

    script_path = os.path.join('scripts', 'test_app2.py')

    if not os.path.exists(script_path):
        return jsonify({'error': 'Test script not found.'}), 400

    def generate_output():
        process = subprocess.Popen(
            ['python', script_path, device_id, android_ver, account_number, pin, amount, phone_number],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in iter(process.stdout.readline, ''):
            yield f"data: {line.strip()}\n\n"

        process.stdout.close()
        process.wait()

    return Response(stream_with_context(generate_output()), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)