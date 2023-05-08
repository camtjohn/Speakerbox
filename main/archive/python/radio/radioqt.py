import time
import os
import sys
import RPi.GPIO as GPIO
import navfolders
import sdcalls, bluecalls
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

#pyqt GUI setup class
class mainView (QWidget):
    def __init__(self):
        super(mainView,self).__init__()
        self.initUI()
        
    def initUI(self):
        
        btn1 = QPushButton('SD',self)
        btn1.move(15,10)
        btn1.setStyleSheet("color:red")
        btn1.clicked.connect(callBtn1)
        btn1.clicked.connect(self.new_window)
        
        btn2 = QPushButton('Bluetooth',self)
        btn2.move(15,40)
        btn2.setStyleSheet("color:blue")
        btn2.clicked.connect(callBtn2)
        
        btn3 = QPushButton('FM radio',self)
        btn3.move(15,70)
        btn3.setStyleSheet("color:green")
        btn3.clicked.connect(callBtn3)

        btn4 = QPushButton('AUX',self)
        btn4.move(15,100)
        btn4.setStyleSheet("color:purple")
        btn4.clicked.connect(callBtn4)
        
        qbtn=QPushButton('GIT!',self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150,50)
        
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('PiRadio')
        self.show()
        
    def new_window(self):
        self.dialog=sdView()
        self.dialog.show()
        
    def close_window(self):
        self.dialog=sdView()
        self.dialog.close()


class sdView (QWidget):
    def __init__(self):
        super(sdView,self).__init__()
        self.initUI()

    def initUI(self):
        
        btn1a=QPushButton(sdcalls.directory[sdcalls.i].currentitems[0],self)
        btn1a.move(15,10)
        btn1a.clicked.connect(callBtn1)
        
        btn2a=QPushButton(sdcalls.directory[sdcalls.i].currentitems[1],self)
        btn2a.move(15,50)
        btn2a.clicked.connect(callBtn2)
        
        btn3a=QPushButton(sdcalls.directory[sdcalls.i].currentitems[2],self)
        btn3a.move(15,90)
        btn3a.clicked.connect(callBtn3)

        btn4a=QPushButton(sdcalls.directory[sdcalls.i].currentitems[3],self)
        btn4a.move(15,130)
        btn4a.clicked.connect(callBtn4)
        
        btn5a=QPushButton('Scroll /\ ',self)
        btn5a.move(15,200)
        btn5a.clicked.connect(callBtn5)
        
        btn6a=QPushButton('Scroll \/ ',self)
        btn6a.move(15,240)
        btn6a.clicked.connect(callBtn6)
                          
        btn7a=QPushButton('Back Directory',self)
        btn7a.move(15,300)
        btn7a.clicked.connect(callBtn7)
        
        qbtna=QPushButton('GIT!',self)
        qbtna.clicked.connect(QApplication.instance().quit)
        qbtna.resize(qbtna.sizeHint())
        qbtna.move(150,300)
        
        #print window_mode
        self.setGeometry(300,300,250,350)
        self.setWindowTitle('sdNavigate')


# Create variable that designates which window is current. Use to assign
# callbacks to buttons. Also, initialize main screen.
list_window_modes=['main', 'sd_navfolder', 'sd_play']
window_mode=list_window_modes[0]

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
    
def callBtn1():
    filter_calls(1)
    
def callBtn2():
    filter_calls(2)
    
def callBtn3():
    filter_calls(3)

def callBtn4():
    filter_calls(4)

def callBtn5():
    filter_calls(5)

def callBtn6():
    filter_calls(6)

def callBtn7():
    filter_calls(7)


# Button press pipes through following filter. Directs the callback to
# diffrent functions based on the current window mode.

def filter_calls(btn):
    global window_mode
    if window_mode=='main':
        if btn==1:
            window_mode=list_window_modes[1]
            sdcalls.start_sd()
            flashLed()
            window1.new_window()

        elif btn==2: bluecalls.blue_out(); print window_mode
        elif btn==3: print '\n FM radio'
        elif btn==4: print '\n Aux selected'
        elif btn==5: print '\n URL Stream selected'

    elif window_mode=='sd_navfolder':
        if btn>0 and btn<=4:
            sdcalls.select_item(btn)
            window1.new_window()
            flashLed()
        elif btn==5 or btn==6:
            sdcalls.navigate(btn)
            window1.new_window()
            flashLed()
        else:
            if sdcalls.i>0:
                sdcalls.backdir()
                window1.new_window()
            else:
                window1.close_window()
                window_mode=list_window_modes[0]
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
    app=QApplication(sys.argv)
    window1=mainView()
    sys.exit(app.exec_())
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
      