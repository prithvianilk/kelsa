# kelsa

- to track and analysis my work and time
- basically: my computer tells me what i'm doing → kafka → pinot → pretty charts that make me feel bad about my productivity

## Desktop Recorder Setup

The desktop recorder captures your computer activity and sends it to the Kelsa API for tracking and analysis.

### Configuration

Create a `config.env` file in the `desktop-recorder/` directory with the following values:

```bash
API_URL=http://your-server-ip:8000
USERNAME=your-username
PASSWORD=your-password
```

#### Required Configuration Values:

- **`API_URL`**: The URL of your Kelsa web application API endpoint
  - Format: `http://IP_ADDRESS:8000` or `https://your-domain.com`
  - Example: `http://65.0.0.0:8000`

- **`USERNAME`**: Your authentication username

- **`PASSWORD`**: Your authentication password

### Running the Desktop Recorder

1. Create your `config.env` file with the required values
2. Install dependencies: `pip install -r desktop-recorder/requirements.txt`
3. Run the recorder: `python desktop-recorder/main.py`

The recorder will start capturing your desktop activity and send data to your Kelsa instance for tracking and analysis.