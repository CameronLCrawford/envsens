# Envsens

## Summary
This is an environment sensor server for a local network. It is designed to run on a Raspberry Pi and performs the following functions:
- Collects data from environment sensors over RPI's GPIO pins
- Stores said data in a database
- Hosts a frontend that displays relevant data

## Further detail

### Database
The database uses [TinyFlux](https://github.com/citrusvanilla/tinyflux) as it is optimised for continuously writing data and subsequently reading that data using queries focused on time. The database instance is a server that accepts and serves two connections in parallel: a process writing to the database (environment sensor data) and a process reading from the database (API). Since both of these processes are running locally, UNIX sockets are used to effectively communicate with these processes.

### API
The API runs using [Flask](https://flask.palletsprojects.com/en/2.2.x/) and has endpoints for various GET requests. [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) is used to allow API access from the frontend.

### Frontend
This is built with [Svelte](https://svelte.dev) and uses [Chart.js](https://www.chartjs.org) for graphs representing time-series data. Using [mDNS](https://en.wikipedia.org/wiki/Multicast_DNS) for resolution and [nginx](https://www.nginx.com) for forwarding, the application can be found at the URL `envsens.local` on the local network.

## Installation
The first stage of installation is cloning this repository.

A handful of python libraries not included in the RPI standard library (installed using pip) are used; these are as follows:
- flask
- flask-cors
- tinyflux
- adafruit_dht

Optionally, nginx can be installed and configured to forward port 8080 to port 80.

## Running
In order to run the project, there are three servers that must be started, as well as the program for recording the environment sensor data. 

1. The first server to run is `database.py` and this is started by running `python3 database/database.py`
2. The second server is the API. This is started using `python3 api/api.py`
3. The third server is the frontend which is started from the `frontend` directory with the command `npm run build && npm start`