#!/usr/bin/python3

import time, os, sys, vlc
import RPi.GPIO as GPIO
import navfolders, sd_module, bluetooth_module, player_module
import wiringpi as wiringpi
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

# Class that designates which window is current and assigns button labels
class GUI_window():
    
    def __init__(self):
        self.current_window = 'main'
        self.btn_label = ['SD','Bluetooth','FM Radio','AUX', 'REBOOT', 'SHUTDOWN', ' ']
        self.label_txt = ['']
    
    def window_config(self, mode):
        player_class = player_module.player_class

        if mode=='main':
            self.current_window='main'
            self.btn_label=['SD','Bluetooth','FM Radio','AUX', 'REpaint', 'quit', player_class.player_button_text]
            self.label_txt = ['']
        
        elif mode=='sd':
            self.current_window = 'sd'
            sd_labels = sd_module.sd_class.current_dir_class.currentitems
            self.btn_label = [sd_labels[0], sd_labels[1], sd_labels[2], sd_labels[3], 'Scroll /\ ', 'Scroll \/ ', 'Navigate back']
            self.label_txt = ['']
        
        elif mode=='player':
            self.current_window='player'          
            self.btn_label=[player_class.pause_button_text, player_class.current_song_title, 'Skip Forward', 'Skip Back', 'Volume Up', 'Volume Down', 'Show Music List']
            self.label_txt = [player_class.volume_label]
        
        #trigger update to GUI labels
        window.trigger_event()

window_class = GUI_window()

#pyqt GUI setup class
class ButtonPressed(QObject):
    pressed = pyqtSignal()

class mainView (QWidget):
    
    def __init__(self):
        super(mainView,self).__init__()
        self.initUI()
        
    def initUI(self):
        btn_label = window_class.btn_label
        label_txt = window_class.label_txt
        
        vertical = 20
        group1_spacing = 90
        group2_spacing = 120
        
        btn1_horiz = 120
        btn2_horiz = btn1_horiz + group1_spacing
        btn3_horiz = btn2_horiz + group1_spacing
        btn4_horiz = btn3_horiz + group1_spacing
        btn5_horiz = btn4_horiz + group2_spacing
        btn6_horiz = btn5_horiz + group1_spacing
        btn7_horiz = btn6_horiz + group2_spacing
        
        self.btn1 = QPushButton(btn_label[0], self)
        self.btn1.move(vertical, btn1_horiz)
        self.btn1.setStyleSheet("color:red")
        self.btn1.clicked.connect(callBtn1)
        
        self.btn2 = QPushButton(btn_label[1], self)
        self.btn2.move(vertical, btn2_horiz)
        self.btn2.setStyleSheet("color:blue")
        self.btn2.clicked.connect(callBtn2)
        
        self.btn3 = QPushButton(btn_label[2], self)
        self.btn3.move(vertical, btn3_horiz)
        self.btn3.setStyleSheet("color:green")
        self.btn3.clicked.connect(callBtn3)

        self.btn4 = QPushButton(btn_label[3], self)
        self.btn4.move(vertical, btn4_horiz)
        self.btn4.setStyleSheet("color:purple")
        self.btn4.clicked.connect(callBtn4)
        
        self.btn5= QPushButton(btn_label[4], self)
        self.btn5.move(vertical, btn5_horiz)
        self.btn5.setStyleSheet("color:orange")
        self.btn5.clicked.connect(callBtn5)       

        self.btn6 = QPushButton(btn_label[5], self)
        self.btn6.move(vertical, btn6_horiz)
        self.btn6.setStyleSheet("color:orange")
        self.btn6.clicked.connect(callBtn6)
        
        self.btn7=QPushButton(btn_label[6], self)
        self.btn7.move(vertical, btn7_horiz)
        #self.btn7.move(300, btn6_horiz)
        self.btn7.clicked.connect(callBtn7)


        #self.label1 = QLabel('Main', self)
        #self.label1.move(vertical, btn1_horiz-9)
        
        self.volume_label = QLabel(label_txt[0], self)
        self.volume_label.move(vertical + 250, (btn5_horiz + btn6_horiz)/2 )

        self.c = ButtonPressed()
        self.c.pressed.connect(self.update_label)
        
        self.setGeometry(0,0,480,800)
        #self.setCursor(QCursor)
        self.setStyleSheet("font: 24pt;background-color:white")
        
        # start in fullscreen
        self.showFullScreen()
        
        #self.show()

    def trigger_event(self):
        self.c.pressed.emit()    
        
    def update_label(self):
        
        btn_label = window_class.btn_label
        label_txt = window_class.label_txt
        
        self.btn1.setText(btn_label[0])
        self.btn2.setText(btn_label[1])
        self.btn3.setText(btn_label[2])
        self.btn4.setText(btn_label[3])
        self.btn5.setText(btn_label[4])
        self.btn6.setText(btn_label[5])
        self.btn7.setText(btn_label[6])
        
        self.volume_label.setText(label_txt[0])
        
        self.btn1.adjustSize()
        self.btn2.adjustSize()
        self.btn3.adjustSize()
        self.btn4.adjustSize()
        self.btn5.adjustSize()
        self.btn6.adjustSize()
        self.btn7.adjustSize()
        self.volume_label.adjustSize()

    def create_playlist(self, mp3_file):
        playlist = QMediaPlaylist()
        url = QUrl.fromLocalFile(url)
        playlist.addMedia(QMediaContent(mp3_file))
        playlist.setPlayBackMode(QMediaPlaylist.Loop)
        
        player = QMediaPlayer()
        player.setPlaylist(playlist)
        player.play()

# ioConfiguration GPIO assignments
BtnPin1 = 4
BtnPin2 = 17
BtnPin3 = 27
BtnPin4 = 5
BtnPin5 = 6
BtnPin6 = 16
BtnPin7 = 26

'''
# Setup i2c module wiringpi
pin_base=65
i2c_addr=0x21
wiringpi.wiringPiSetup()
wiringpi.pcf8574Setup(pin_base, i2c_addr)


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

def flashLed():
    wiringpi.digitalWrite(LedPin,led_on)
    time.sleep(.5)
    wiringpi.digitalWrite(LedPin,led_off)
'''    


# Button press pipes through following filter. Directs the callback to
# diffrent functions based on the current window mode.

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


def filter_calls(btn):

    current_window = window_class.current_window
    sd_class = sd_module.sd_class
    item_type = sd_class.item_type
    
    if current_window=='main':
        if btn==1:
            window_class.window_config('sd')

        elif btn==2:
            bluetooth_module.blue_out()
        elif btn==3: print('\n FM radio')
        elif btn==4: print('\n Aux selected')
        #elif btn==5: os.system('sudo reboot now')
        elif btn==5: window_class.window_config('main')
        #elif btn==6: os.system('sudo shutdown now')
        elif btn==6:
            app.quit()
            
        elif btn==7 and player_module.player_class.player_button_text=='Player View':
            window_class.window_config('player')


    elif current_window=='sd':
        
        if btn>0 and btn<=4: #Select item (folder or file)
            sd_class.select_item(btn)
            
            #if item is folder, show sd screen next, if file show player view
            if sd_class.item_type=='folder': window_class.window_config('sd')
            elif sd_class.item_type=='file':
                player_module.player_class.play_selected_file()
                window_class.window_config('player')

        elif btn==5 or btn==6: #Navigate through list
            if btn==5: sd_class.current_dir_class.navigatelist('backward')
            elif btn==6: sd_class.current_dir_class.navigatelist('forward')
            
            window_class.window_config('sd')


        elif btn==7: #navigate back one directory (or back to 'Main')
            dir_lvl = sd_class.dir_lvl
            if dir_lvl == 0: window_class.window_config('main')
            
            else:
                sd_class.dir_lvl -= 1
                sd_class.current_dir_class = sd_class.directory[sd_class.dir_lvl]
                window_class.window_config('sd')
                
                
        elif btn==8: #Show 'Player' screen
            if player_module.player_class.player_button_text=='Player View':
                window_class.window_config('player')
                
    
    elif current_window=='player':
        player_class = player_module.player_class
        
        if btn==1: #if paused=play and turn button to 'pause', if playing=pause and turn button to 'play'
            player_class.play_pause_song()
            window_class.window_config('player')

        elif btn==2:
            print('unassigned')
            
        elif btn==3: #play next song in playlist
            player_class.next_song()
            window_class.window_config('player')
                
        elif btn==4: #play previous song in playlist
            player_class.previous_song()
            window_class.window_config('player')
            
        elif btn==5:
            player_class.volume_control('up')
            window_class.window_config('player')

        elif btn==6:
            player_class.volume_control('down')
            window_class.window_config('player')
            
        elif btn==7:
            window_class.window_config('sd')        


# setup buttons button press
def setup():
    GPIO.setmode(GPIO.BCM) #Use GPIOnumber (not 1-40)
    GPIO.setup(BtnPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Btnpin mod is input, pulled up to 3.3v
    GPIO.setup(BtnPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # wait for falling, set bouncetime to prevent callback calling multiple times when btn pressed
    GPIO.add_event_detect(BtnPin1, GPIO.FALLING, callback=callBtn1, bouncetime=400)
    GPIO.add_event_detect(BtnPin2, GPIO.FALLING, callback=callBtn2, bouncetime=400)
    GPIO.add_event_detect(BtnPin3, GPIO.FALLING, callback=callBtn3, bouncetime=400)
    GPIO.add_event_detect(BtnPin4, GPIO.FALLING, callback=callBtn4, bouncetime=400)
    GPIO.add_event_detect(BtnPin5, GPIO.FALLING, callback=callBtn5, bouncetime=400)
    GPIO.add_event_detect(BtnPin6, GPIO.FALLING, callback=callBtn6, bouncetime=400)
    GPIO.add_event_detect(BtnPin7, GPIO.FALLING, callback=callBtn7, bouncetime=400)

app = 0  
def qt():
    global app
    global window
    app=QApplication(sys.argv)
    window=mainView()
    sys.exit(app.exec_())


# start program!
if __name__== '__main__':
    setup()
    qt()
    GPIO.cleanup()
