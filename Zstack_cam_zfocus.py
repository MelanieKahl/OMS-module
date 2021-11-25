# LED Imports
#import RPi.GPIO as GPIO   # necessary for use of GPIO pins
from time import sleep
from picamera import PiCamera
from fractions import Fraction
import serial

## --- LED Settings ---
# define using boardnumbers (1-14) oder GPIO numbers
#GPIO.setmode(GPIO.BCM)   # using GPIO numbers
# Define Pin als Output
#GPIO.setup(15, GPIO.OUT)    # GPIO 15 / Board-Pin 10 - Ground 6
#GPIO.setup(24, GPIO.OUT)    # GPIO 24 / Board-Pin 18 - Ground 14

## RAMPS Settings#
#ramps = serial.Serial('/dev/ttyACM0', 250000)  # define Port and Baudrate
#print(ramps.name, 'is online')  # check Port's name

#cam = PiCamera(
#    resolution=(2028, 1520),
#    framerate=Fraction(1, 6),
#    sensor_mode=3)
#cam.shutter_speed = 200000
#cam.iso = 600

folder='/home/pi/'
imgName='test01'

GPIO.output(15, GPIO.HIGH)

sleep(2)
cam.capture("%s%s.bmp" % (folder, imgName))
sleep(2)
GPIO.output(15, GPIO.LOW)

print("Image captured in", folder, imgName)


# By contrast, this code closes the camera between shots (but can’t use the convenient capture_continuous() method as a result):
#for i in range(60):
#    sleep(1) # Camera warm-up time
#    filename = 'image%02d.bmp' % i
#    cam.capture(filename)
#    print('Captured %s' % filename)
#    # Capture one image a minute
#    time.sleep(59)

ramps.write(b'G91\n')  # Set to relative mode
print('Set to relative mode')  # print a question

cam.start_preview()
cam.preview.alpha = 240

# Turn blue LED ON
GPIO.output(15, GPIO.HIGH)


# G0 E1 --> 5 µm
# G0 E2 --> 10 µm

for i in range(10):
    sleep(1) # Camera warm-up time
    ramps.write(b'G0 E2\n')    # move Z Focus Stage um 10 µm
    sleep(2)
    filename = 'image%02d.bmp' % i
    cam.capture(filename)
    print('Captured %s' % filename)
    # Capture one image a minute
    sleep(1)

# Turn blue LED OFF
GPIO.output(15, GPIO.LOW)
cam.stop_preview()
