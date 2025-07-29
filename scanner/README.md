# Barcode Scanner

A barcode scanner using Python and OpenCV.

## Features
 
1. List available cameras `--list`.
2. Decode barcodes and qrcodes.
3. Decoded payload can be published to MQTT  `--mqtt`.
4. Decoding process can be visualized in webbrowser `--http`.
 


## Instalation

1. Install Python3 and in an installer add it to Path

	https://www.python.org/downloads/


2. Check if your python works by typing `python3` in console


3. If you don't have pip you need to install it by this command:

	python -m ensurepip --upgrade

   If it didin't work, you need to use second option that is described here: https://pip.pypa.io/en/stable/installation/
4. Install OpenCV for Python:

	pip install opencv-python


5. `pyzbar` - a Python library for barcode and QR code reading:	

	pip install pyzbar


6. `paho-mqtt` - a Python MQTT client library:

	pip install paho-mqtt


7. `StringUtils` - a library to validate, manipulate and generate strings:

	pip install python-string-utils

8. Read the comments in scanner.py, they might be usefull if something didin't work


9. To use chip Reader you need to uncomment 2 libraries in chip_reader.py


10. On your raspberry pi you need to install mqtt broker like Mosquitto and node-red 

## Usage 

1. Decode barcodes and qrcodes.

	scanner> python scanner.py 

2. Decoded payload can be published to MQTT.

	scanner> python scanner.py --mqtt=localhost

3. Decoding process can be visualized in webbrowser. 
Start [http://localhost:8000](http://localhost:8000) to visualize decoding process.

	scanner> python stream.py --http 

4. If you don't know if your camera is working use:

	scanner> python stream.py --list