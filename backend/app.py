from flask import Flask, render_template, request, jsonify
from vm_manager import list_vms, start_vm, stop_vm, create_vm

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vms', methods=['GET'])
def get_vms():
    vms = list_vms()
    return render_template('vm_list.html', vms=vms)

@app.route('/start', methods=['POST'])
def start_virtual_machine():
    vm_name = request.json.get('vm_name')
    success = start_vm(vm_name)
    return jsonify({"success": success})

@app.route('/stop', methods=['POST'])
def stop_virtual_machine():
    vm_name = request.json.get('vm_name')
    success = stop_vm(vm_name)
    return jsonify({"success": success})

@app.route('/create', methods=['POST'])
def create_virtual_machine():
    data = request.json
    vm_name = data.get('vm_name')
    memory = data.get('memory')  # in MB
    vcpus = data.get('vcpus')
    success = create_vm(vm_name, memory, vcpus)
    return jsonify({"success": success})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
