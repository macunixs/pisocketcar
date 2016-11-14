import time
import RPi.GPIO as GPIO
# Import the PCA9685 module.
import Adafruit_PCA9685

from flask import *
from flask_socketio import SocketIO

# L298N to GPIO mapping
##DRIVE_EN12 ====> channel 0
DRIVE_1A = 17
DRIVE_2A = 27

##DRIVE_EN34 =====> channel 1
DRIVE_4A = 5
DRIVE_3A = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(DRIVE_1A, GPIO.OUT)  # left wheel
GPIO.setup(DRIVE_2A, GPIO.OUT)  # left wheel

GPIO.setup(DRIVE_3A, GPIO.OUT)  # right wheel
GPIO.setup(DRIVE_4A, GPIO.OUT)  # right wheel

pwm = Adafruit_PCA9685.PCA9685()
left = 0
right = 0
motor1 = 0       # LEFT channel 0
motor2 = 1       # RIGHT channel 1


# Create flask app, SocketIO object, and global pi 'thing' object.
app = Flask(__name__)
socketio = SocketIO(app)

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Define app routes.
# Index route renders the main HTML page.
@app.route("/")
def index():
    return render_template('goaccelero.html')

@socketio.on('drive')
def get_drive(driveleft,driveright):
    print('leftspeed:{0} || rightspeed:{1}'.format(driveleft,driveright))
    if driveleft > 0 and driveright > 0:
        GPIO.output(DRIVE_1A, GPIO.HIGH)
        GPIO.output(DRIVE_4A, GPIO.HIGH)
        GPIO.output(DRIVE_2A, GPIO.LOW)
        GPIO.output(DRIVE_3A, GPIO.LOW)
        left = driveleft
        right = driveright

    elif driveleft < 0 and driveright < 0:
        GPIO.output(DRIVE_1A, GPIO.LOW)
        GPIO.output(DRIVE_4A, GPIO.LOW)
        GPIO.output(DRIVE_2A, GPIO.HIGH)
        GPIO.output(DRIVE_3A, GPIO.HIGH)
        left = -driveleft 
        right = -driveright

    elif driveleft > 0 and driveright < 0:  # turn right      left >0 && right <0
        GPIO.output(DRIVE_1A, GPIO.LOW)
        GPIO.output(DRIVE_4A, GPIO.HIGH)
        GPIO.output(DRIVE_2A, GPIO.HIGH)
        GPIO.output(DRIVE_3A, GPIO.LOW)
        left = driveleft 
        right = -driveright 
    else:                                   # turn left       right >0 && left <0
        GPIO.output(DRIVE_1A, GPIO.HIGH)
        GPIO.output(DRIVE_4A, GPIO.LOW)
        GPIO.output(DRIVE_2A, GPIO.LOW)
        GPIO.output(DRIVE_3A, GPIO.HIGH)
        left = -driveleft 
        right = driveright 

    pwm.set_pwm(0, 0, int(left))        # left wheel
    pwm.set_pwm(1, 0, int(right))        # right wheel



if __name__ == "__main__":
    try:
        pwm.set_pwm_freq(60)
        socketio.run(app, host='0.0.0.0', port = 9000, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()

