# Kelsa

**An app to auto track and analyze my work and time**

> My computer tells me what I'm doing → Kafka → Pinot → pretty charts that make me feel bad about my productivity

## Configuration

### Desktop Recorder

Create `config.env` in the project root or configure via environment variables:

- **`API_URL`**: Web app endpoint (e.g., `http://localhost:8000`)
- **`USERNAME`**: Authentication username
- **`PASSWORD`**: Authentication password

#### Setting up as a LaunchAgent (macOS)

To have the desktop recorder start automatically at login:

1. Make the desktop-recorder script executable:
   ```bash
   chmod +x /path/to/kelsa/desktop-recorder/desktop-recorder.sh
   ```

2. Copy the `com.prithvianilk.kelsa.desktop_recorder_startup.plist` file to `~/Library/LaunchAgents`:
   ```bash
   cp com.prithvianilk.kelsa.desktop_recorder_startup.plist ~/Library/LaunchAgents/
   ```

3. Load the LaunchAgent:
   ```bash
   launchctl load -w ~/Library/LaunchAgents/com.prithvianilk.kelsa.desktop_recorder_startup.plist
   ```

4. To verify it's running:
   ```bash
   launchctl list | grep kelsa
   ```

5. For troubleshooting, check the log files:
   ```bash
   cat /tmp/kelsa-desktop-recorder.log
   cat /tmp/kelsa-desktop-recorder.err
   ```

### Web App

Create `config.env` in the project root or configure via environment variables:

- **`HTPASSWD_FILE`**: The path to the htpasswd file (e.g., `~/users/me/kelsa/pinot/data/nginx/.htpasswd`)