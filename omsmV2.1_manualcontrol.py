# Tkinter Imports
import tkinter as tk           # alias: name tkinter as tk (its just short)
from tkinter import ttk       # ttk is a set of widgets, buttons, styles, etc... 
import tkinter.font as font

# LED Imports
import RPi.GPIO as GPIO   # necessary for use of GPIO pins
from time import sleep

# Camera Imports
from picamera import PiCamera
from fractions import Fraction

cam = PiCamera(
    resolution=(2028, 1520),
    framerate=Fraction(1, 6),
    sensor_mode=3)


## --- LED Settings --- 
# define using boardnumbers (1-14) oder GPIO numbers
GPIO.setmode(GPIO.BCM)   # using GPIO numbers
# Define Pin als Output
GPIO.setup(15, GPIO.OUT)    # GPIO 15 / Board-Pin 10 - Ground 6
GPIO.setup(24, GPIO.OUT)    # GPIO 24 / Board-Pin 18 - Ground 14

## RAMPS Settings#
import serial
ramps = serial.Serial('/dev/ttyACM0', 250000)  # define Port and Baudrate
print(ramps.name, 'is online')  # check Port's name

## --- Class Camera ---

class OMSMClass(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     # essentially the same as self = tk.Tk()

        self.title("OMSM V1.2")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ## - Variables to be shared between classes -
        self.iso_value = tk.IntVar(value=400)
        self.shutter_value = tk.IntVar(value=100000)
        self.storagelocation = tk.StringVar(value="/home/pi/")
        self.imagename = tk.StringVar()
        # --------------

        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight=1)

        camera_frame = CameraSettings(container, self)
        camera_frame.grid(row=0, column=0, padx=50, pady=25, sticky="NSEW")
        
        xyz_frame = XYZZstage(container, self)
        xyz_frame.grid(row=0, column=1, padx=50, pady=25, sticky="NSEW")


class CameraSettings(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)

        self.controller = controller

        style = ttk.Style(self)
        style.theme_use("clam")

        settings_label = ttk.Label(self, text="Camera Settings", font='bold')
        settings_label.grid(row=0, column=0, columnspan=3)
        
        # ISO
        iso_label = ttk.Label(self, text="ISO")
        iso_label.grid(row=1, column=0, rowspan=2)
        
        s#elf.iso_value = tk.IntVar(value=400)   # in the controller

        iso_one = ttk.Radiobutton(
            self,
            text="ISO 200",
            variable=controller.iso_value,
            value=200
        )
        iso_two = ttk.Radiobutton(
            self,
            text="ISO 400",
            variable=controller.iso_value,
            value=400
        )
        iso_three = ttk.Radiobutton(
            self,
            text="ISO 600",
            variable=controller.iso_value,   # all variable have the same storage_variable!
            value=600 
        )        
        iso_four = ttk.Radiobutton(
            self,
            text="ISO 800",
            variable=controller.iso_value,   # all variable have the same storage_variable!
            value=800         # this way they belong together
        )

        iso_one.grid(row=1, column=1)
        iso_two.grid(row=1, column=2)
        iso_three.grid(row=2, column=1)
        iso_four.grid(row=2, column=2)

        # Shutter
        shutter_label = ttk.Label(self, text="Shutterspeed")
        shutter_label.grid(row=3, column=0)

        #self.shutter_value = tk.IntVar(value=100000)
        shutter_box = ttk.Entry(self, width=12, textvariable=controller.shutter_value)
        shutter_box.grid(row=3, column=1)

        # Image Savings
        #self.storagelocation = tk.StringVar(value="/home/pi/")
        #self.imagename = tk.StringVar()

        image_savings = ttk.Label(self, text="Image Saving Options", font=("Segoe UI", 12))
        image_savings.grid(row=4, column=0, columnspan=2)

        storagelocation_label = ttk.Label(self, text="Storage Location:")
        storagelocation_label.grid(row=5, column=0)
        storagelocation_entry = ttk.Entry(self, width=12, textvariable=controller.storagelocation)
        storagelocation_entry.grid(row=5, column=1)

        imagename_label = ttk.Label(self, text="Image Name:")
        imagename_label.grid(row=6, column=0)
        imagename_entry = ttk.Entry(self, width=12, textvariable=controller.imagename)
        imagename_entry.grid(row=6, column=1)

        # Save Settings
        save_button = ttk.Button(self, text='Save Settings', command=self.savings)
        save_button.grid(row=7, column=0, columnspan=3, sticky="EW")

        # Snapshots
        snapshots_title = ttk.Label(self, text="Take Snapshots", font='bold')
        snapshots_title.grid(row=0, column=3)

        blue_button = ttk.Button(
            self, 
            text='Snapshot - Blue Light', 
            command=self.blue_snapshot
            )

        blue_button.grid(row=1, column=3)

        mint_button = ttk.Button(
            self, 
            text='Snapshot - Mint Light', 
            command=self.mint_snapshot
            )

        mint_button.grid(row=2, column=3)

        both_button = ttk.Button(
            self, 
            text='Snapshot - both Lights', 
            command=self.both_snapshot
            )

        both_button.grid(row=3, column=3)

        preview_title = ttk.Label(self, text="Live Image", font='bold')
        preview_title.grid(row=5, column=3)

        start_button = ttk.Button(
            self, 
            text='Start', 
            command=self.start_live
            )

        stop_button = ttk.Button(
            self, 
            text='Stop', 
            command=self.stop_live
            )

        start_button.grid(row=6, column=3)
        stop_button.grid(row=7, column=3)



        for child in self.winfo_children():
                child.grid_configure(padx=5, pady=5)

    def savings(self, *args):
        print("ISO:", self.controller.iso_value.get())
        print("Shutter Speed:", self.controller.shutter_value.get())
        print("Storage Location:", self.controller.storagelocation.get())
        print("Image Name:", self.controller.imagename.get())


    def both_snapshot(self, *args):
        cam.shutter_speed = self.controller.shutter_value.get()
        cam.iso = self.controller.iso_value.get()
        folder=self.controller.storagelocation.get()
        imgName=self.controller.imagename.get()
        GPIO.output(15, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        sleep(2)
        cam.capture("%s%s.bmp" % (folder, imgName))
        sleep(2)
        GPIO.output(15, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        print("Image captured in", folder, imgName)
        print("ISO:", self.controller.iso_value.get())
        print("Shutterspeed:", self.controller.shutter_value.get())

    def blue_snapshot(self, *args):
        cam.shutter_speed = self.controller.shutter_value.get()
        cam.iso = self.controller.iso_value.get()
        folder=self.controller.storagelocation.get()
        imgName=self.controller.imagename.get()
        GPIO.output(15, GPIO.HIGH)
        sleep(2)
        cam.capture("%s%s.bmp" % (folder, imgName))
        sleep(2)
        GPIO.output(15, GPIO.LOW)
        print("Image captured in", folder, imgName)
        print("ISO:", self.controller.iso_value.get())
        print("Shutterspeed:", self.controller.shutter_value.get())

    def mint_snapshot(self, *args):
        cam.shutter_speed = self.controller.shutter_value.get()
        cam.iso = self.controller.iso_value.get()
        folder=self.controller.storagelocation.get()
        imgName=self.controller.imagename.get()
        GPIO.output(24, GPIO.HIGH)
        sleep(2)
        cam.capture("%s%s.bmp" % (folder, imgName))
        sleep(2)
        GPIO.output(24, GPIO.LOW)
        print("Image captured in", folder, imgName)
        print("ISO:", self.controller.iso_value.get())
        print("Shutterspeed:", self.controller.shutter_value.get())

    def start_live(self, *args):
        cam.shutter_speed = self.controller.shutter_value.get()
        cam.iso = self.controller.iso_value.get()
        GPIO.output(15, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        sleep(1)
        cam.start_preview()
        cam.preview.alpha = 240

    def stop_live(self, *args):
        GPIO.output(15, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        sleep(1)
        cam.stop_preview()


class XYZZstage(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)

        self.controller = controller

        titel_label = ttk.Label(self, text='XYZz Stage', font='bold')
        titel_label.grid(row=0, column=0, columnspan=2)

        xy_label = ttk.Label(self, text='Move in X and Y direction')
        xy_label.grid(row=1, column=0, columnspan=2)

        ymax_button = ttk.Button(self, text='Y max', command=self.ymax)
        xmin_button = ttk.Button(self, text='X min', command=self.xmin)
        xmax_button = ttk.Button(self, text='X max', command=self.xmax)
        ymin_button = ttk.Button(self, text='Y min', command=self.ymin)

        ymax_button.grid(row=2, column=1, sticky="EW")
        xmin_button.grid(row=3, column=0, sticky="EW")
        xmax_button.grid(row=3, column=2, sticky="EW")
        ymin_button.grid(row=4, column=1, sticky="EW")

        zz_label = ttk.Label(self, text='Move in Z direction')
        zz_label.grid(row=5, column=0, columnspan=2)

        zcoarseup_button = ttk.Button(self, text='Z coarse up', command=self.zcoarseup)
        zcoarsedown_button = ttk.Button(self, text='Z coarse down', command=self.zcoarsedown)
        zfineup_button = ttk.Button(self, text='Z fine up', command=self.zfineup)
        zfinedown_button = ttk.Button(self, text='Z fine down', command=self.zfinedown)

        zcoarseup_button.grid(row=6, column=0, sticky="EW")
        zcoarsedown_button.grid(row=7, column=0, sticky="EW")
        zfineup_button.grid(row=6, column=1, sticky="EW")
        zfinedown_button.grid(row=7, column=1, sticky="EW")

        home_label = ttk.Label(self, text='Homing')
        home_label.grid(row=8, column=0, columnspan=2)

        xhome_button = ttk.Button(self, text='Home X', command=self.xhome)
        yhome_button = ttk.Button(self, text='Home Y', command=self.yhome)
        zhome_button = ttk.Button(self, text='Home Z', command=self.zhome)
        xyzhome_button = ttk.Button(self, text='Home X Y and Z stage', command=self.xyzhome)

        xhome_button.grid(row=9, column=0, sticky="EW")
        yhome_button.grid(row=9, column=1, sticky="EW")
        zhome_button.grid(row=9, column=2, sticky="EW")
        xyzhome_button.grid(row=10, column=0, columnspan=3, sticky="EW")

        for child in self.winfo_children():
                child.grid_configure(padx=5, pady=5)

    def ymax(self, *args):
        print('Move Y stage up')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 Y10 \n')
        sleep(1)

    def xmin(self, *args):
        print('Move X stage down')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 X-10 \n')
        sleep(1)

    def xmax(self, *args):
        print('Move X stage up')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 X10 \n')
        sleep(1)

    def ymin(self, *args):
        print('Move Y stage down')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 Y-10 \n')
        sleep(1)

    def zcoarseup(self, *args):
        print('Move Z coarse stage up')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 Z-5 \n')
        sleep(1)

    def zcoarsedown(self, *args):
        print('Move Z coarse stage down')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 Z5 \n')
        sleep(1)

    def zfineup(self, *args):
        print('Move Z fine stage up')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 E5 \n')
        sleep(1)

    def zfinedown(self, *args):
        print('Move Z fine stage down')
        ramps.write(b'G91\n') # set to relative mode
        ramps.write(b'G0 E-5 \n')
        sleep(1)

    def xhome(self, *args):
        print('Home X stage')
        ramps.write(b'G28 X\n')
        sleep(10)

    def yhome(self, *args):
        print('Home Y stage')
        ramps.write(b'G28 Y\n')
        sleep(10)

    def zhome(self, *args):
        print('Home Z stage')
        ramps.write(b'G28 Z\n')
        sleep(10)

    def xyzhome(self, *args):
        print('Home all stages')
        ramps.write(b'G28\n')
        sleep(10)


## ---  TKinter ---
# create Main Window
root = OMSMClass()

root.mainloop()
