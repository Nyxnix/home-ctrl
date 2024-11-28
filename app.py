from flask import Flask, jsonify, request, render_template
import paramiko
import time

app = Flask(__name__)

# Tesira SSH info
HOST = "192.168.1.183"
USER = "default"
PASSWORD = ""

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
        #time.sleep(2)
        output = ssh_shell.recv(1024).decode('utf-8').strip()
        print(f"Command output: {output}")
        return output
    except Exception as e:
        print(f"Error sending command: {e}")
        return "error"

# Commands
def get_status():
    try:
        raw_status = sendCommand("Level1 get mute 1")
        if '+OK "value":true' in raw_status:
            return "muted"
        elif '+OK "value":false' in raw_status:
            return "unmuted"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def toggle_microphone():
    try:
        return sendCommand("Level1 toggle mute 1")
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def mute_microphone():
    try:
        return sendCommand("Level1 set mute 1 true")
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def unmute_microphone():
    try:
        return sendCommand("Level1 set mute 1 false")
    except Exception as e:
        print(f"Error: {e}")
        return "error"

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_status", methods=["POST"])
def get_status_route():
    status = get_status()
    return jsonify({"status": status})

@app.route("/toggle_microphone", methods=["POST"])
def toggle_microphone_route():
    result = toggle_microphone()
    return jsonify({"status": get_status()})

@app.route("/mute_microphone", methods=["POST"])
def mute_microphone_route():
    result = mute_microphone()
    return jsonify({"status": get_status()})

@app.route("/unmute_microphone", methods=["POST"])
def unmute_microphone_route():
    result = unmute_microphone()
    return jsonify({"status": get_status()})

if __name__ == "__main__":
    app.run(debug=True)
