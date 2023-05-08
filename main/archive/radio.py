import time
import os
import RPi.GPIO as GPIO
import navfolders
import sdcalls, bluecalls


# Create variable that designates which window is current. Use to assign
# callbacks to buttons. Also, initialize main screen.

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


# ioConfiguration GPIO assignments

BtnPin1=17
BtnPin2=18
BtnPin3=19
BtnPin4=20
LedPin=21
BtnPin5=22
BtnPin6=23
BtnPin7=24

Led_status=0


# Button callback functions

def flashLed():
    GPIO.output(LedPin,1)
    time.sleep(.1)
    GPIO.output(LedPin,0)
    
def callBtn1(ev=None):
    filter_calls(1)
    
def callBtn2(ev=None):
    filter_calls(2)
    
def callBtn3(ev=None):
    filter_calls(3)

def callBtn4(ev=None):
    filter_calls(4)

def callBtn5(ev=None):
    filter_calls(5)

def callBtn6(ev=None):
    filter_calls(6)

def callBtn7(ev=None):
    filter_calls(7)


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



def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BtnPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Btnpin mod is input, pulled up to 3.3v
    GPIO.setup(BtnPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LedPin, GPIO.OUT)
    GPIO.setup(BtnPin5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def loop():
    # wait for falling, set bouncetime to prevent callback calling multiple times when btn pressed
    GPIO.add_event_detect(BtnPin1, GPIO.FALLING, callback=callBtn1, bouncetime=200)
    GPIO.add_event_detect(BtnPin2, GPIO.FALLING, callback=callBtn2, bouncetime=200)
    GPIO.add_event_detect(BtnPin3, GPIO.FALLING, callback=callBtn3, bouncetime=200)
    GPIO.add_event_detect(BtnPin4, GPIO.FALLING, callback=callBtn4, bouncetime=200)
    GPIO.add_event_detect(BtnPin5, GPIO.FALLING, callback=callBtn5, bouncetime=200)
    GPIO.add_event_detect(BtnPin6, GPIO.FALLING, callback=callBtn6, bouncetime=200)
    GPIO.add_event_detect(BtnPin7, GPIO.FALLING, callback=callBtn7, bouncetime=200)
    while True:
        time.sleep(1)
        
def destroy():
    GPIO.cleanup()


# start program!
if __name__== '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        