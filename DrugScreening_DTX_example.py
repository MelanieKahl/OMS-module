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

## __________ Stack 1 ______________
## Z stack with mint and blue Light

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C2a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C2a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 2 ______________
## Z stack with mint and blue Light

# Move to next Well
ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C3')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C3a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C3a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 3 ______________
## Z stack with mint and blue Light

# Move to next Well
ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C4')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C4a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C4a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 4 ______________
## Z stack with mint and blue Light

# Move to next Well
ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C5')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C5a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C5a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 5 ______________
## Z stack with mint and blue Light

# Move to next Well
ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C6')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C6a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C6a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 6 ______________
## Z stack with mint and blue Light

ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C7')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C7a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C7a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 7 ______________
## Z stack with mint and blue Light

ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C8')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C8a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C8a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 8 ______________
## Z stack with mint and blue Light

ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C9')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C9a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C9a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)

## __________ Stack 9 ______________
## Z stack with mint and blue Light

ramps.write(b'G0 Y144\n')
sleep(10)
print('moved to Well C10')

for i in range(51):
    ramps.write(b'G91\n')               # set to relative mode
    ramps.write(b'G0 E2\n')             # move Z focus
    cam.shutter_speed = 150000
    cam.iso = 400
    GPIO.output(mintLED, GPIO.HIGH)     # Mint LED on
    filenameM = '20220512_DTX3_P1_C10a_mi_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameM)
    sleep(0.3)
    GPIO.output(mintLED, GPIO.LOW)      # Mint LED off
    cam.shutter_speed = 180000
    cam.iso = 600
    sleep(0.3)
    GPIO.output(blueLED, GPIO.HIGH)     # Blue LED on
    filenameB = '20220512_DTX3_P1_C10a_bl_%02d.bmp' % i
    sleep(1)
    cam.capture(filenameB)
    print('Captured:', i)
    sleep(0.3)
    GPIO.output(blueLED, GPIO.LOW)     # Blue LED off

ramps.write(b'G91\n')
ramps.write(b'G0 E-102\n')
sleep(2)
cam.stop_preview()
sleep(1)
ramps.write(b'G0 Y-1152\n')
sleep(20)

# _______Close_________________________
ramps.close()