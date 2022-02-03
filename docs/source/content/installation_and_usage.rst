**********************
Installation and Usage
**********************

.. _installation:

Prerequisites
#############

.. note::
   You should have installed Python 3 and pip3 installed.

Mosquitto Broker Installation
=============================
First of all, you should have installed ``mosquitto``. To install it, go to their official website and download and install the Mosquitto Broker for your OS.

For Ubuntu/Debian:
-----
1. Install Mosquitto using:

.. code-block:: console

   sudo apt update
   sudo apt install mosquitto

2. To check whether the service is running or not and to start it, run:

.. code-block:: console

   sudo systemctl status mosquitto # Checking if the service is running
   sudo systemctl start mosquitto # Start the service

For Mac OS:
-----
1. Install Mosquitto on Mac OS using Homebrew:

.. code-block:: console

   brew install mosquitto

For Windows (WSL):
-----
To install Mosquitto on Windows Subsystem for Linux (version 2), use the same 
commands as the ones for the Ubuntu/Debian installation (if you're using a 
Ubuntu/Debian WSL distribution). To run the broker with ``systemctl``, you have to 
run your WSL shell with ``systemd``, because WSL does not start with it by default. 
You can check out this tutorial on how to start your WSL with ``systemd``. After 
this step, you can run the same commands as the ones in the Ubuntu/Debian 
installation steps to check if the broker is running or start it.


Installation
############

1. Create a virtual envirionment using 

.. code-block:: console

   python3 -m venv venv

2. Activate the envirionment using

.. code-block:: console

   .\venv\Scripts\activate # for Windows
   source venv/bin/activate # for Unix

3. Install the requirements from ``requirements.txt`` using 
   
.. code-block:: console

   (venv) pip install -r requirements.txt

4. Select development mode for server:

.. code-block:: console

   (venv) export FLASK_ENV=development


Usage 
#####

To start the MQTT Broker service run:

.. code-block:: console

   mosquitto

or 

.. code-block:: console

   sudo systemctl start mosquitto

To run the Flask server, start it with:

.. code-block:: console

   (venv) python app.py


Swagger API
===========

To access the Swagger API, access http://localhost:500/apidocs/ and enjoy
all of your oven's features.


Testing
#######

You can run our tests by:

1. Starting the MQTT Broker service by running:

.. code-block:: console

   mosquitto

2. Activating the environment using

.. code-block:: console

   .\venv\Scripts\activate # for Windows
   source venv/bin/activate # for Unix
   
3. We created 32 unit tests. You can run them by using this command in the project root folder:

.. code-block:: console
   
   pytest tests-unit/

4. If you want to run the unit tests and check the code coverage you can run:

.. code-block:: console

   cd ..
   pytest --cov=SmartOven SmartOven/tests-unit/

You can find our results `here <https://github.com/banana-breads/SmartOven/blob/master/docs/unit_tests_coverage.png>`_.

5. We created 2 intergation tests. You can run them by using this command in the project root folder:

.. code-blcok:: console

   pytest tests-integration/

6. If you want to run the intergation tests and check the code coverage you can run:

.. code-block:: console
   
   cd ..
   pytest --cov=SmartOven SmartOven/tests-integration/
   
You can find our results `here <https://github.com/banana-breads/SmartOven/blob/master/docs/integration_tests_coverage.png>`_.


Automation Tests
================

To run the automation tests provided for this project, you should have a Postman account
and access `this link <https://smartoven.postman.co/workspace/SmartOven-IoT~3965cbb7-e5be-43a9-8974-8701218a8c51>`_
to run them. Select the environment coresponding to the collection you want to run and after than, select a collection 
and choose `Run collection`.













