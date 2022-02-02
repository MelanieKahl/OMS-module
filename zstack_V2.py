# LED Imports
import RPi.GPIO as GPIO   # necessary for use of GPIO pins
from time import sleep
from picamera import PiCamera
from fractions import Fraction
import serial

## --- LED Settings --- 
# define using boardnumbers (1-14) oder GPIO numbers
blueLED = 15
mintLED = 24

GPIO.setmode(GPIO.BCM)   # using GPIO numbers
# Define Pin als Output
GPIO.setup(blueLED, GPIO.OUT)    # GPIO 15 / Board-Pin 10 - Ground 6
GPIO.setup(mintLED, GPIO.OUT)    # GPIO 24 / Board-Pin 18 - Ground 14

## RAMPS Settings#
ramps = serial.Serial('/dev/ttyACM0', 250000)  # define Port and Baudrate
print(ramps.name, 'is online')  # check Port's name

# Camera Settings
cam = PiCamera(
    resolution=(2028, 1520),
    framerate=Fraction(1, 6),
    sensor_mode=3)

sleep(1)
ramps.write(b'G91\n')  # Set to relative mode
print('Set to relative mode')  # print a question

cam.start_preview()
cam.preview.alpha = 240

for i in range(61):
    sleep(1)
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    sleep(1)
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220130_R2_D4_mi_E2_%02d.bmp' % i
    sleep(2)
    cam.capture(filenameM)
    sleep(1)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 200000
    cam.iso = 600
    sleep(1)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220130_R2_D4_bl_E2_%02d.bmp' % i
    sleep(2)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(1)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G0 E-121\n')
cam.stop_preview()
ramps.close()