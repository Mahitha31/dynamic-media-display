# dynamic-media-display
Dynamic Media Display System Using Raspberry Pi
A web-controlled slideshow system for displaying images on a connected screen using a Raspberry Pi. The system supports:

-Real-time web control via a browser
-Dynamic directory selection
-Customizable delay between images
-Full-screen slideshow using feh
-Start/Stop slideshow with a single click

Features
-Web-based control panel hosted on the Raspberry Pi
-Selection of image directories
-Configurable slideshow delay (in seconds)
-Remote start and stop functionality
-Lightweight and easy to deploy

Folder Structure
dynamic-media-display/
├── slideshow.py         # Main Python file to run the webserver and slideshow
├── media/               # Default folder to store images
└── README.md            # Project documentation

Requirements
-Raspberry Pi with a desktop environment (GUI)
-Python 3.x
-feh image viewer

Install feh using the following command:
sudo apt-get update
sudo apt-get install feh

How to Run
Clone or copy the repository to your Raspberry Pi.
Ensure the /home/pi/media folder or another valid directory contains image files.

Execute the following command to start the application:
python3 slideshow.py
Open a web browser on any device connected to the same local network and navigate to:


http://<raspberry-pi-ip>:8000
(For example: http://192.168.1.102:8000, as shown in the terminal when the server starts.)

