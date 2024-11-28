from flask import Flask, jsonify, request, render_template
import paramiko
import time

app = Flask(__name__)

# Need to make a lot of these vars assignable from the web page, but im lazy rn
# Tesira SSH info
HOST = "192.168.1.183"
USER = "default"
PASSWORD = ""

# Tesira Instance Tag/index assign
LevelBlockTag = "Level1"
LevelBlockIndex = "1"
MixerBlockTag = "Mixer1"

# stuff that only applies to my tesira :)
micInIndex = "1"
guitarInIndex = "2"

outLIndex = "3"
outRIndex = "4"

# Global variables
ssh_client = None
ssh_shell = None

def makeShell():
    global ssh_client, ssh_shell
    try:
        if ssh_client is None or not ssh_client.get_transport() or not ssh_client.get_transport().is_active():
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=HOST, port=22, username=USER, password=PASSWORD)
            ssh_shell = ssh_client.invoke_shell()
            time.sleep(3)  # Allow the shell to initialize
            print("Shell ready!")
        return ssh_shell
    except Exception as e:
        print(f"Error establishing SSH shell: {e}")
        ssh_client = None
        ssh_shell = None
        return None

def sendCommand(command):
    global ssh_shell
    try:
        if ssh_shell is None:
            makeShell()

        ssh_shell.send(command + '\n')
        time.sleep(0.1)
        output = ssh_shell.recv(1024).decode('utf-8').strip()
        print(f"Command output: {output}")
        return output
    except Exception as e:
        print(f"Error sending command: {e}")
        return "error"

# Commands
def get_mic_status():
    try:
        micStatus = sendCommand(f"{LevelBlockTag} get mute {LevelBlockIndex}")
        if '+OK "value":true' in micStatus:
            return jsonify({"status": "muted"})
        elif '+OK "value":false' in micStatus:
            return jsonify({"status": "unmuted"})
        else:
            return jsonify({"status": "unknown"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"})


def get_mic_monitor_status():
    try:
        micMonitorStatus = sendCommand(f"{MixerBlockTag} get crosspointLevelState {micInIndex} {outLIndex}")
        if '+OK "value":true' in micMonitorStatus:
            return jsonify({"status": "active"})
        elif '+OK "value":false' in micMonitorStatus:
            return jsonify({"status": "inactive"})
        else:
            return jsonify({"status": "unknown"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"})


def toggle_microphone():
    try:
        return sendCommand(f"{LevelBlockTag} toggle mute {LevelBlockIndex}")
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def mute_microphone():
    try:
        return sendCommand(f"{LevelBlockTag} set mute {LevelBlockIndex} true")
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def unmute_microphone():
    try:
        return sendCommand(f"{LevelBlockTag} set mute {LevelBlockIndex} false")
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def micMonitorToggle():
    try:
        sendCommand(f"{MixerBlockTag} toggle crosspointLevelState {micInIndex} {outLIndex}")
        sendCommand(f"{MixerBlockTag} toggle crosspointLevelState {micInIndex} {outRIndex}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def guitarMonitorToggle():
    try:
        sendCommand(f"{MixerBlockTag} toggle crosspointLevelState {guitarInIndex} {outLIndex}")
        sendCommand(f"{MixerBlockTag} toggle crosspointLevelState {guitarInIndex} {outRIndex}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return "error"

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_all_statuses", methods=["POST"])
def get_all_statuses():
    try:
        mic_status = get_mic_status_json().get_json()["status"]
        mic_monitor_status = get_mic_monitor_status_json().get_json()["status"]
        guitar_monitor_status = get_guitar_monitor_status_json().get_json()["status"]

        return jsonify({
            "mic_status": mic_status,
            "mic_monitor_status": mic_monitor_status,
            "guitar_monitor_status": guitar_monitor_status
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "mic_status": "error",
            "mic_monitor_status": "error",
            "guitar_monitor_status": "error"
        })


# Helper functions to fetch individual status as JSON (for reuse)
def get_mic_status_json():
    return get_mic_status()

def get_mic_monitor_status_json():
    return get_mic_monitor_status()

def get_guitar_monitor_status_json():
    try:
        guitarMonitorStatus = sendCommand(f"{MixerBlockTag} get crosspointLevelState {guitarInIndex} {outLIndex}")
        if '+OK "value":true' in guitarMonitorStatus:
            return jsonify({"status": "muted"})
        elif '+OK "value":false' in guitarMonitorStatus:
            return jsonify({"status": "unmuted"})
        else:
            return jsonify({"status": "unknown"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"})

@app.route("/toggle_microphone", methods=["POST"])
def toggle_microphone_route():
    result = toggle_microphone()
    return jsonify({"status": get_mic_status()})

@app.route("/mute_microphone", methods=["POST"])
def mute_microphone_route():
    try:
        result = mute_microphone()

        mic_status_response = get_mic_status()
        mic_status_data = mic_status_response.get_json()  # Extract JSON data

        return jsonify({"status": mic_status_data["status"]})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"})

@app.route("/unmute_microphone", methods=["POST"])
def unmute_microphone_route():
    try:
        result = unmute_microphone()

        mic_status_response = get_mic_status()
        mic_status_data = mic_status_response.get_json()  # Extract JSON data

        return jsonify({"status": mic_status_data["status"]})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"})


@app.route("/mic_monitor", methods=["POST"])
def toggle_mic_monitor_route():
    result = micMonitorToggle()
    return jsonify({"status": get_mic_monitor_status()})

@app.route("/guitar_monitor", methods=["POST"])
def toggle_guitar_monitor_route():
    result = guitarMonitorToggle()
    return jsonify({"status": get_guitar_monitor_status()})

if __name__ == "__main__":
    app.run(debug=True)
