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
DRIVE_1A = 17
DRIVE_2A = 27

##DRIVE_EN34 =====> channel 1
DRIVE_4A = 5
DRIVE_3A = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.setup(DRIVE_1A, GPIO.OUT)  # left wheel
GPIO.setup(DRIVE_2A, GPIO.OUT)  # left wheel

GPIO.setup(DRIVE_3A, GPIO.OUT)  # right wheel
GPIO.setup(DRIVE_4A, GPIO.OUT)  # right wheel

pwm = Adafruit_PCA9685.PCA9685()
pwmbuzz = Adafruit_PCA9685.PCA9685()

left = 0
right = 0
motor1 = 0       # LEFT channel 0
motor2 = 1       # RIGHT channel 1
buzzer = 3
multiplier = 1
running = True
all_clear = True
# metric_distance = 200

@app.route("/")
def index():
    return render_template('gyrosocket.html')

@socketio.on('drive')
def get_drive(driveleft,driveright):
    global count
    count+=1
    print("socket {0}:    {1}    |    {2} ".format(count,driveleft,driveright))

    driveleft = multiplier * driveleft
    driveright = multiplier * driveright
    # print('leftspeed:{0} || rightspeed:{1}'.format(driveleft,driveright))
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

        GPIO.output(DRIVE_1A, GPIO.HIGH)
        GPIO.output(DRIVE_4A, GPIO.LOW)
        GPIO.output(DRIVE_2A, GPIO.LOW)
        GPIO.output(DRIVE_3A, GPIO.HIGH)
        left = driveleft
        right = -driveright
    else:                                   # turn left       right >0 && left <0

        GPIO.output(DRIVE_1A, GPIO.LOW)
        GPIO.output(DRIVE_4A, GPIO.HIGH)
        GPIO.output(DRIVE_2A, GPIO.HIGH)
        GPIO.output(DRIVE_3A, GPIO.LOW)
        left = -driveleft
        right = driveright


    # if metric_distance < 10 :
    #     # GPIO.output(DRIVE_1A, GPIO.HIGH)
    #     # GPIO.output(DRIVE_4A, GPIO.HIGH)
    #     # GPIO.output(DRIVE_2A, GPIO.LOW)
    #     # GPIO.output(DRIVE_3A, GPIO.LOW)
    #     pwm.set_pwm(0, 0, left)        # left wheel
    #     pwm.set_pwm(1, 0, right)        # right wheel
    # else:
    pwm.set_pwm(0, 0, int(left))        # left wheel
    pwm.set_pwm(1, 0, int(right))        # right wheel
    running = True

def proximity():
    global all_clear, metric_distance
    # metric_distance = 100
    while running:
        value = sensor.Measurement(trig_pin, echo_pin)
        raw_measurement = value.raw_distance(sample_size=5, sample_wait=0.03)
        # Calculate the distance in centimeters
        metric_distance = value.distance_metric(raw_measurement)
        buzz = metric_distance * 64
        print("distance = {} centimeters".format(metric_distance))
        if metric_distance > 50:
            GPIO.output(red, GPIO.HIGH)
            GPIO.output(green, GPIO.HIGH)
            GPIO.output(blue, GPIO.LOW)
            pwmbuzz.set_pwm(buzzer, 0, 0)        # buzz off


        elif metric_distance > 30 and metric_distance < 50:
            GPIO.output(red, GPIO.HIGH)
            GPIO.output(green, GPIO.LOW)
            GPIO.output(blue, GPIO.HIGH)
            pwmbuzz.set_pwm(buzzer, 0, 0)        # buzz off


        else :
            all_clear = False
            GPIO.output(red, GPIO.LOW)
            GPIO.output(green, GPIO.HIGH)
            GPIO.output(blue, GPIO.HIGH)
            pwmbuzz.set_pwm(buzzer, 2048, int(buzz))        # buzz on


            time.sleep(0.05)
            GPIO.output(red, GPIO.HIGH)
            GPIO.output(green, GPIO.HIGH)
            GPIO.output(blue, GPIO.HIGH)
            pwmbuzz.set_pwm(buzzer, 0, 0)        # buzz off

            time.sleep(0.001)
        # else:
        #     time.sleep(5)
        #     pwm.set_pwm(0, 0, 0)        # left wheel
        #     pwm.set_pwm(1, 0, 0)        # right wheel


if __name__ == "__main__":
    try:
        t1 = Thread(target=proximity)
        t1.start()
        pwm.set_pwm_freq(60)
        pwmbuzz.set_pwm_freq(6000)

        socketio.run(app, host='0.0.0.0', port = 9000, debug=True)
    finally:
        t1.stop()
        GPIO.cleanup()
        
