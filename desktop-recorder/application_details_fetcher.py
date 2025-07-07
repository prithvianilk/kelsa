from abc import abstractmethod
import subprocess
import json
import Quartz

class ApplicationDetailsFetcher:
    def __init__(self):
        pass

    @abstractmethod
    def get_active_application_details(self):
        pass

    def is_user_active(self, idle_threshold_seconds=1):
        """Checks if the user has been active in the last `idle_threshold_seconds`."""
        idle_time = Quartz.CGEventSourceSecondsSinceLastEventType(
            Quartz.kCGEventSourceStateHIDSystemState, Quartz.kCGAnyInputEventType
        )
        return idle_time < idle_threshold_seconds

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
            return data.get('application'), data.get('tab'), self.is_user_active()
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError) as e:
            # If the script fails, print the error for debugging
            if isinstance(e, subprocess.CalledProcessError):
                print(f"DEBUG: JXA script failed with return code {e.returncode}")
                print(f"DEBUG: stderr: {e.stderr}")
            else:
                print(f"DEBUG: Python error after JXA script execution: {e}")
            return None, None, False

class AppleScriptApplicationDetailsFetcher(ApplicationDetailsFetcher):
    def get_active_application_details(self):
        applescript = """
        tell application "System Events"
            set front_app to first application process whose frontmost is true
            set app_name to name of front_app
            set window_title to ""
            try
                if (exists (window 1 of front_app)) then
                    set window_title to name of window 1 of front_app
                end if
            end try
            return "{\\"application\\":\\"" & app_name & "\\", \\"tab\\":\\"" & window_title & "\\"}"
        end tell
        """
        try:
            cmd = ['osascript', '-e', applescript]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout.strip())
            return data.get('application'), data.get('tab'), self.is_user_active()
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError) as e:
            if isinstance(e, subprocess.CalledProcessError):
                print(f"DEBUG: AppleScript failed with return code {e.returncode}")
                print(f"DEBUG: stderr: {e.stderr}")
            else:
                print(f"DEBUG: Python error after AppleScript execution: {e}")
            return None, None, False