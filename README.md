<!-- README template used: https://github.com/othneildrew/Best-README-Template -->

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Forks][forks-shield]][forks-url]
[![MIT License][license-shield]][license-url]

<h3 align="center">SmartOven</h3>
  <p align="center">
    Oven. But smart.
  </p>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#usage">Testing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

SmartOven is an IoT project which aims to make baking a simpler and more enjoyable experience. 

SmartOven's developers are 
<a href="https://github.com/mehanix">Nicoleta Ciaușu</a>,
<a href="https://github.com/Nicu-Ducal">Nicolae Ducal</a>,
<a href="https://github.com/Stefan-Radu">Ștefan Radu</a> and
<a href="https://github.com/lauratender">Laura Tender</a>.

This project was developed during the Software Engineering Course at University of Bucharest under guidance of our teacher <a href="https://github.com/raresito">Rareș Cristea</a>.

For more information about our project you can also check our [SmartOven's online Documentation](https://smartoven.readthedocs.io/en/latest/) and the [Customer Requirements Analysis Document](https://github.com/banana-breads/SmartOven/blob/update-customer-analysis-doc/docs/Document_de_analiza_a_cerintelor_clientului__SmartOven.pdf).
<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [MongoDb](https://www.mongodb.com/)
* [Eclipse Mosquitto](https://mosquitto.org/)
* [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [pytest](https://docs.pytest.org/en/6.2.x/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
You should have [python3](https://www.python.org/downloads/) and [pip3](https://pypi.org/project/pip/) installed.

You should also install mosquitto broker.
#### Mosquitto Broker Installation
To install the Mosquitto, go to their [official website](https://mosquitto.org/download/) and download and install the Mosquitto Broker for your OS.

#### For Ubuntu/Debian:
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

#### For Mac: 
Install Mosquitto on Mac OS using Homebrew:
```bash
brew install mosquitto
```

#### For Windows (WSL):
To install Mosquitto on Windows Subsystem for Linux (version 2), use the same commands as the ones for the Ubuntu/Debian installation (if you're using a Ubuntu/Debian WSL distribution). To run the broker, you have to run your WSL shell with `systemd`, because WSL does not start with it by default. You can check out [this tutorial](https://github.com/DamionGans/ubuntu-wsl2-systemd-script) on how to start your WSL with `systemd`. After this step, you can run the same commands as the ones in the Ubuntu/Debian installation steps to check if the broker is running or start it.

### Installation
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

4. Select development mode for server:
```bash
export FLASK_ENV=development
```

<!-- USAGE EXAMPLES -->
## Usage
To start the MQTT Broker service run:
```bash
mosquitto
```

To run the Flask server, start it with
```bash
python app.py
```
or you can run it in test mode (be sure to remove all of the elements from the test database you are running in test mode):
```bash
python app.py --test 
```

To create a new device, run
```bash
python device.py
```
if the server exists, it will connect automatically.

#### Swagger API
To access the Swagger API, access [http://localhost:5000/apidocs/]() and enjoy all of your oven's features.
<p align="right">(<a href="#top">back to top</a>)</p>

## Testing
You can run our tests by:

1. Starting the MQTT Broker service by running:
```bash
mosquitto
```

2. Activating the environment using
```bash
.\venv\Scripts\activate # for Windows
source venv/bin/activate # for Unix
```

3. Using this command in the project root folder:
```bash
pytest tests/
```

4. If you want to run the tests and check the coverage you can run:
```bash
cd ..
```
```bash
pytest --cov=SmartOven SmartOven/tests/
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Team [banana-breads](https://github.com/banana-breads)

Project Link: [https://github.com/banana-breads/SmartOven](https://github.com/banana-breads/SmartOven)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Some resources we found helpful and we want to give credit to are:

* The Software Engineering Courses from University of Bucharest
* [SmartBed Example Project from the Software Engineering course](https://github.com/raresito/SmartBed-RESTApi-example)
* [Flask Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
* [Flask Project Layout](https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/)
* [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/tutorial.html)
* [PyTest Documentation](https://docs.pytest.org/en/6.2.x/contents.html)
* [Pytest-cov documentation](https://pytest-cov.readthedocs.io/en/latest/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/banana-breads/SmartOven.svg?style=for-the-badge
[contributors-url]: https://github.com/banana-breads/banana-breads/SmartOven/graphs/contributors

[stars-shield]: https://img.shields.io/github/stars/banana-breads/SmartOven.svg?style=for-the-badge
[stars-url]: https://github.com/banana-breads/SmartOven/stargazers

[issues-shield]: https://img.shields.io/github/issues/banana-breads/SmartOven.svg?style=for-the-badge
[issues-url]: https://github.com/banana-breads/SmartOven/issues

[license-shield]: https://img.shields.io/github/license/banana-breads/SmartOven.svg?style=for-the-badge
[license-url]: https://github.com/banana-breads/SmartOven/blob/master/LICENSE

[forks-shield]: https://img.shields.io/github/forks/banana-breads/SmartOven.svg?style=for-the-badge
[forks-url]: https://github.com/banana-breads/SmartOven/network/members
