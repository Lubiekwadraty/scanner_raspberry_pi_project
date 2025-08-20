# Barcode Scanner

A barcode scanner using Python and OpenCV.

A visualization in a web browser.

A React app that gets message from mqtt and sends message to server through the api.

An Express server that's connect to mariaDB database and sends there an action that user selected in react app

## Features
 
1. List available cameras `--list`.
2. Decode barcodes and qrcodes.
3. Decoded payload can be published to MQTT  `--mqtt`.
4. Decoding process can be visualized in web browser `--http`.
5. Decoding rfid card and chips `--chip`.
 


## Instalation for scanner

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


9. To use chip Reader you need to uncomment 2 libraries in `chip_reader.py`


10. On your raspberry pi you need to install mqtt broker like Mosquitto and optionally node-red 

11. The `MFRC522.py` file it's not my own file, it's a python library that you can't install using `sudo apt install`. Original library you can get there, this library is optional, I'm using it only for `chip_reader.py` https://pypi.org/project/mfrc522-python/.



## Usage 

1. Decode barcodes and qrcodes.

	scanner> python scanner.py 

2. Decoded payload can be published to MQTT.

	scanner> python scanner.py --mqtt=localhost

3. Decoding process can be visualized in webbrowser. 
Start [http://localhost:8000](http://localhost:8000) to visualize decoding process.

	scanner> python scanner.py --http 

4. If you don't know if your camera is working use:

	scanner> python scanner.py --list

## Instalation for React app

1. You need to install node.js

	https://nodejs.org/en/download/

2. In `app` folder use command `npm install`, this will install every package that react app needs:

	app> npm install

## usage

1. use command `npm run dev` to run it, after that console will show you a local url and network url for lan usage:

	app> npm run dev

## Instalation for Express server

1. You need to install node.js if you didin't do it:

	https://nodejs.org/en/download/

2. In `server` folder use command `npm install`, this will install every package that express app needs:

	server> npm install

3. You need to install MariaDB database on your computer or raspberry pi (where you want to use this app).

	-If you want to use your computer for this you can just download `XAMPP control panel` from this link: https://www.apachefriends.org/ or just MariaDB.

	-If you want to use raspberry pi for this you need to install MariaDB using this command: `sudo apt-get install mariadb-server -y`. After that if you try to login into mariaDB with this command `mysql -u root -p`, you will get an error - acces denied. You need to change this if if you want the database to work properly with the server. To change this you need to login with sudo `sudo mysql -u root` and after this make this command: `GRANT ALL PRIVILEGES on *.* to 'root'@'localhost' IDENTIFIED BY '<password>';` replacing password with your desired mysql root password and the second command: `FLUSH PRIVILEGES;`.
	You need to set this password also in `const pool` in `server/app.js`.

4. In server folder there is file `database.txt` there all commands you need to use in MariaDB for your database. There's also inserts commands that you can use for test.

5. use command `node app.js` to run it:

	server> node app.js


## MQTT broker

1. For that i'm using mosquitto https://mosquitto.org/download/

2. In order to use it you need to `modify mosquitto.conf` file with this lines:

		listener 1883
		protocol mqtt

		listener 9001
		protocol websockets
		
		allow_anonymous true

## Using raspberry pi

#### &ensp; for better usage you can download putty and connect it with your raspberry pi by ssh, it's usefull when you need 4 sessions at once.

## Node-red
 &ensp;  I also used node-red for beep sound after message sent by mqtt, but it's optional.
 ![alt text](image-1.png)

## Rfid reader
&ensp; This is how you need to connect rfid reader
![alt text](image.png)
https://pypi.org/project/mfrc522-python/#connections


# Final effect

### to connect all of this and run final app you need to make 3 commands in 3 diffrent terminals:

1. In scanner folder use this command:

&emsp; &emsp; &emsp; `python3 scanner.py --mqtt=localhost` if you want you 
can use also other arguments but
&emsp; &emsp; &emsp; mqtt is crucial for 2 other parts.

2. In app folder use `npm run dev`

3. In server folder use `node app.js`

4. Remember to turn on MariaDB. On computer in Xammp you only need to click start on `mySQL`