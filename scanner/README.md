# Barcode Scanner

A barcode scanner using Python and OpenCV.

## Features
 
1. List available cameras `--list`.
2. Decode barcodes and qrcodes.
3. Decoded payload can be published to MQTT  `--mqtt`.
4. Decoding process can be visualized in webbrowser `--http`.
 


## Instalation

1. Install Python3 and add to Path
2. Install OpenCV for Python:

	pip install opencv-python

3. `pyzbar` - a Python library for barcode and QR code reading:	

	pip install pyzbar


4. `paho-mqtt` - a Python MQTT client library:

	pip install paho-mqtt

5. `StringUtils` - a library to validate, manipulate and generate strings:

	pip install python-string-utils



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