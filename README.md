# SmartOven
Oven. But smart.

# Installation
## Mosquitto Broker Installation
To install the Mosquitto, go to their [official website](https://mosquitto.org/download/) and download and install the Mosquitto Broker for your OS.

### For Ubuntu/Debian:
Install Mosquitto using:
```bash
sudo apt update
sudo apt install mosquitto
```
To check whether the service is running or not and to start it, run:
```bash
sudo systemctl status mosquitto # Checking if the service is running
sudo systemctl start mosquitto # Start the service
```

### For Mac: 
Install Mosquitto on Mac OS using Homebrew:
```bash
brew install mosquitto
```

### For Windows (WSL):
To install Mosquitto on Windows Subsystem for Linux (version 2), use the same commands as the ones for the Ubuntu/Debian installation (if you're using a Ubuntu/Debian WSL distribution). To run the broker, you have to run your WSL shell with `systemd`, because WSL does not start with it by default. You can check out [this tutorial](https://github.com/DamionGans/ubuntu-wsl2-systemd-script) on how to start your WSL with `systemd`. After this step, you can run the same commands as the ones in the Ubuntu/Debian installation steps to check if the broker is running or start it.

## Python enviroment
1. Create a virtual environment using 
```bash
python -m venv venv
```

2. Activate the environment using
```bash
.\venv\Scripts\activate # for Windows
source venv/bin/activate # for Unix
```

3. Install the requirements from `requirements.txt` using 
```bash
pip install -r requirements.txt 
```

4. To run the Flask server, start it with
```bash
flask run
```