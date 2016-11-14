from flask import *
from flask_socketio import SocketIO
# Import the PCA9685 module.
import Adafruit_PCA9685
from hcsr04sensor import sensor
from threading import Thread
import time
import RPi.GPIO as GPIO

# Create flask app, SocketIO object
app = Flask(__name__)
socketio = SocketIO(app)
count = 0

trig_pin = 7
echo_pin = 8
red = 21
green = 20
blue = 16
# L298N to GPIO mapping
##DRIVE_EN12 ====> channel 0
IN1 = 17
IN2 = 27

##DRIVE_EN34 =====> channel 1
IN4 = 5
IN3 = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.setup(IN1, GPIO.OUT)  # left wheel
GPIO.setup(IN2, GPIO.OUT)  # left wheel

GPIO.setup(IN3, GPIO.OUT)  # right wheel
GPIO.setup(IN4, GPIO.OUT)  # right wheel

pwm = Adafruit_PCA9685.PCA9685()

left = 0
right = 0
motorL = 0       # LEFT channel 0
motorR = 1       # RIGHT channel 1
buzzer = 3
multiplier = 1
running = True
all_clear = True
# metric_distance = 200

@app.route("/")
def index():
    return render_template('gyroedit.html')

@socketio.on('drive')
def get_drive(driveleft,driveright):
    global count
    count+=1
    print("socket {0}:    {1}    |    {2} ".format(count,driveleft,driveright))

    driveleft = multiplier * driveleft
    driveright = multiplier * driveright
    # print('leftspeed:{0} || rightspeed:{1}'.format(driveleft,driveright))
    if driveleft > 0 and driveright > 0:

        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN4, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)

        left = driveleft
        right = driveright

    elif driveleft < 0 and driveright < 0:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)

        left = -driveleft
        right = -driveright

    elif driveleft > 0 and driveright < 0:  # turn right      left >0 && right <0

        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        left = driveleft
        right = -driveright
    else:                                   # turn left       right >0 && left <0

        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        left = -driveleft
        right = driveright


    pwm.set_pwm(motorL, 0, int(left))        # left wheel
    pwm.set_pwm(motorR, 0, int(right))        # right wheel
    running = True

if __name__ == "__main__":
    try:
        pwm.set_pwm_freq(60)
        socketio.run(app, host='0.0.0.0', port = 9000, debug=True)
    finally:
        GPIO.cleanup()
