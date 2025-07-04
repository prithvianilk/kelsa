import json
from kafka import KafkaProducer
import time
import subprocess

# TODO: Does not work for all apps. Cursor is an example.
def get_active_window_info():
    """
    Gets the name of the currently active application and its window title
    using JavaScript for Automation (JXA).
    """
    jxa_script = """
    function run() {
        var se = Application("System Events");
        var frontmost_app_name = se.applicationProcesses.where({ frontmost: true }).name()[0];
        var frontmost_app = Application(frontmost_app_name);

        var window_title = "";
        try {
            if (frontmost_app.windows.length > 0) {
                window_title = frontmost_app.windows[0].name();
            }
        } catch (e) {
            // This application may not support JXA's 'windows' property.
        }

        return JSON.stringify({application: frontmost_app_name, tab: window_title});
    }
    """
    try:
        cmd = ['osascript', '-l', 'JavaScript', '-e', jxa_script]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout.strip())
        return data.get('application'), data.get('tab')
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError) as e:
        # If the script fails, print the error for debugging
        if isinstance(e, subprocess.CalledProcessError):
            print(f"DEBUG: JXA script failed with return code {e.returncode}")
            print(f"DEBUG: stderr: {e.stderr}")
        else:
            print(f"DEBUG: Python error after JXA script execution: {e}")
        return None, None


bootstrap_servers = 'localhost:9094'
topic_name = 'work-topic'

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    request_timeout_ms=1000
)

while True:
    try:
        app, tab = get_active_window_info()
        message_data = {
            "application": app,
            "tab": tab,
            "done_at": int(time.time() * 1000)
        }
        producer.send(topic_name, value=message_data)
        producer.flush()
        print(f"Sent to topic '{topic_name}' with value {message_data}")
    except Exception as e:
        print(f"Error sending message: {e}")
    time.sleep(1)