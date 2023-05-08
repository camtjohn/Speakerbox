#!/usr/bin/python

import time
import os
import RPi.GPIO as GPIO
import navfolders
import sdcalls, bluecalls
import wiringpi as wiringpi


# Setup i2c module wiringpi

pin_base=65
i2c_addr=0x21
wiringpi.wiringPiSetup()
wiringpi.pcf8574Setup(pin_base, i2c_addr)


''' Create variable that designates which window is current. Use to assign
    callbacks to buttons. Also, initialize main screen. '''

list_window_mode=['main', 'sd_navfolder', 'sd_play']

def current_window(mode):
    global window_mode
    window_mode=list_window_mode[mode]
    print window_mode
    # Initialize main window selection screen
    if mode==0:
        os.system('clear')
        print 'SD\nBLUETOOTH\nSPOTIFY\nAUX\nURL STREAM'

current_window(0)


'''ioConfiguration i2c assignments'''

# Base pin is 65, this function allows to input 0-7 to define pin
def pin_mod(pin):
	pin_mod=pin+65
	return pin_mod
	
LedPin=pin_mod(0) # pin0 on i2c expander(pcf8574)

# pull i2c pins 1-8 high
for pin in range(1,8):
    wiringpi.digitalWrite(pin_mod(pin),1)


led_on=0	# Led connected to high, drive low to turn on)
led_off=1	# drive high to turn off


# Button callback functions

def flashLed():
    wiringpi.digitalWrite(LedPin,led_on)
    time.sleep(.5)
    wiringpi.digitalWrite(LedPin,led_off)
    


# Button press pipes through following filter. Directs the callback to
# diffrent functions based on the current window mode.

def filter_calls(btn):
    global window_mode
  
    if window_mode=='main':
        if btn==1:            
            current_window(1)
            sdcalls.start_sd()
            flashLed()

        elif btn==2:
            bluecalls.blue_out()
            flashLed()
            
        elif btn==3: print '\n Spotify selected'
        elif btn==4: print '\n Aux selected'
        elif btn==5: print '\n URL Stream selected'

    elif window_mode=='sd_navfolder':
        if btn>0 and btn<=4:
            sdcalls.select_item(btn)
            flashLed()
        elif btn==5 or btn==6:
            sdcalls.navigate(btn)
            flashLed()
        else:
            if sdcalls.i>0: sdcalls.backdir()
            else: current_window(0)
            flashLed()

    
# poll for button press
def loop():
    while True:
        
        for pin in range(1,8):
            if wiringpi.digitalRead(pin_mod(pin))==0:
                filter_calls(pin)
                time.sleep(.01)

        time.sleep(.1)

def destroy():
    GPIO.cleanup()


# start program!
if __name__== '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        
