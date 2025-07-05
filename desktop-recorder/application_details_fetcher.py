from abc import abstractmethod
import subprocess
import json

class ApplicationDetailsFetcher:
    def __init__(self):
        pass

    @abstractmethod
    def get_active_application_details(self):
        pass

class JxaApplicationDetailsFetcher(ApplicationDetailsFetcher):
    def get_active_application_details(self):
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