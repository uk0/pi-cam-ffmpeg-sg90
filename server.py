from time import sleep
import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
from flask import make_response

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pan = 27
tilt = 17

GPIO.setup(tilt, GPIO.OUT)  # white => TILT
GPIO.setup(pan, GPIO.OUT)  # gray ==> PAN


def setServoAngle(servo, angle):
    assert angle >= 0 and angle <= 180
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.1)
    pwm.stop()


@app.after_request
def af_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route('/lr/<int:x>')
def left_right(x):
    setServoAngle(tilt, x)
    return "{}".format(x)


@app.route('/ud/<int:y>')
def up_down(y):
    setServoAngle(pan, y)

    return "{}".format(y)


# def setServoAngle(servo, angle):
#     pwm = GPIO.PWM(servo, 50)
#     pwm.start(8)
#     dutyCycle = angle / 18. + 3.
#     pwm.ChangeDutyCycle(dutyCycle)
#     sleep(0.3)
#     pwm.stop()


def clean():
    GPIO.cleanup()


# 17 is left right

# 27 up down
if __name__ == '__main__':
    os.system('''nohup ffmpeg -f video4linux2 -s 1024x768 -r 24 -i /dev/video0 -f flv rtmp://xxx.xx.xx.xx:1935/stream/aaa >> /dev/null  &''')
    app.run(host='0.0.0.0', debug=True)
