# Remote control tri-wheel car using WiFi + socketio

# This project will teach you how to build a controllable robot using WiFi.

Requirements to run this project:

<b>
1 - Python3 or Python2
<br>
2 - flask
<br>
3 - flask-socketio
<br>
4 - Adafruit PCA9685
<br>
5 - L298N Full H-Bridge 
<br>
6 - Smartphone with accelerometer support
<br>
7 - WiFi network (local for both Raspberry Pi and the smartphone)
</b>
<h2> All files needed are included. No additional files/installation required other than the modules listed above. </h2>

# Show me how to set the robot up

<code> Will be updated </code>

# How to run it?

Make sure you have all the aforementioned dependencies. Once you've everything setup and ready, just run this code in terminal. 

For Python 2:
<code> sudo python socketcar.py </code>

For Python 3:
<code> sudo python3 socketcar.py </code>

After that, just grab your smartphone and fire up the web browser. Access the webpage by entering the IP address of the Pi with port 9000. (you can change the port number in the code if you want). 

Example:
<code> http://192.168.0.90:9000 </code>

You may need to refresh the page to reload the server.

