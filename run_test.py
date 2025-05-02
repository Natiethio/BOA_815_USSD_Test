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
    pin        = data.get('pin', '').strip()
    amount          = data.get('amount', '').strip()
    phone_number    = data.get('phone_number', '').strip()

    # script = {
    #     'scripts/test_app2',
    # }

    script = os.path.join('scripts','test_app2.py')

    if not os.path.exists(script):
      return jsonify({'error': 'Test script not found.'}), 400
    

    # if not script or not os.path.exists(script):
    #     return jsonify({'error': 'Invalid test case selected.'}), 400

    # Build command args
    cmd = ['python', 
           script, 
           device_id, 
           android_ver, 
           account_number,
           pin,
           amount,
           phone_number 
           ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = proc.stdout
    except subprocess.CalledProcessError as e:
        output = e.stderr

    # Extract “Report saved at:” line if present
    report_path = None
    for line in output.splitlines():
        if 'Report saved at:' in line:
            report_path = line.split('Report saved at:')[-1].strip()
            break
    if not report_path:
        report_path = os.path.abspath('test_results.txt')

    # Append raw output to a simple log
    with open('test_results.txt', 'a', encoding='utf-8') as f:
        f.write(output + "\n\n")

    return jsonify({
        'output':      output,
        'report_path': report_path
    })

if __name__ == '__main__':
    app.run(debug=True)
