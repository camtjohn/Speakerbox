# list files/folders (listqty) at a time, buttons select/navigate
import os
import time
import RPi.GPIO as GPIO


##############
#BUTTON SETUP#
##############

BtnPin1=17
BtnPin2=18
BtnPin3=19
BtnPin4=20
LedPin=21
BtnPin5=22
BtnPin6=23
BtnPin7=24

Led_status=0

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
    
def flashLed():
    GPIO.output(LedPin,1)
    time.sleep(.1)
    GPIO.output(LedPin,0)

def navforward(ev=None):
    print ' '
    directory[i].navigatelist(1)
    flashLed()
    
def navbackward(ev=None):
    print ' '
    directory[i].navigatelist(2)
    flashLed()

def select_item1(ev=None):
    print ' '
    global rootdir
    global i
    selection=os.path.join(os.path.abspath(directory[i].currentdir),directory[i].mergelist[directory[i].list_index+0])
    i+=1
        
    if os.path.isdir(selection):
        rootdir=selection
        directory[i]=navfolders()
        directory[i].listitems(4)
            
    elif os.path.isfile(selection):
        print  'this is file!!'
        
    flashLed()
        
def select_item2(ev=None):
        print ' '
        global rootdir
        global i
        selection=os.path.join(os.path.abspath(directory[i].currentdir),directory[i].mergelist[directory[i].list_index+1])
        i+=1
        
        if os.path.isdir(selection):
            rootdir=selection
            directory[i]=navfolders()
            directory[i].listitems(4)
            
        elif os.path.isfile(selection):
            print  'this is file!!'
        
        flashLed()
        
def select_item3(ev=None):
        print ' '
        global rootdir
        global i
        selection=os.path.join(os.path.abspath(directory[i].currentdir),directory[i].mergelist[directory[i].list_index+2])
        i+=1
        
        if os.path.isdir(selection):
            rootdir=selection
            directory[i]=navfolders()
            directory[i].listitems(4)
            
        elif os.path.isfile(selection):
            print  'this is file!!'
        
        flashLed()

def select_item4(ev=None):
        print ' '
        global rootdir
        global i
        selection=os.path.join(os.path.abspath(directory[i].currentdir),directory[i].mergelist[directory[i].list_index+3])
        i+=1
        
        if os.path.isdir(selection):
            rootdir=selection
            directory[i]=navfolders()
            directory[i].listitems(4)
            
        elif os.path.isfile(selection):
            print  'this is file!!'
        
        flashLed()


def backdir(ev=None):
    print ' '
    global i
    if i>0:
        i-=1
        directory[i].listitems(4)
    else: directory[i].listitems(4)
    
    flashLed()

def loop():
    # wait for falling, set bouncetime to prevent callback calling multiple times when btn pressed
    GPIO.add_event_detect(BtnPin5, GPIO.FALLING, callback=navforward, bouncetime=200)
    GPIO.add_event_detect(BtnPin6, GPIO.FALLING, callback=navbackward, bouncetime=200)
    GPIO.add_event_detect(BtnPin1, GPIO.FALLING, callback=select_item1, bouncetime=200)
    GPIO.add_event_detect(BtnPin2, GPIO.FALLING, callback=select_item2, bouncetime=200)
    GPIO.add_event_detect(BtnPin3, GPIO.FALLING, callback=select_item3, bouncetime=200)
    GPIO.add_event_detect(BtnPin4, GPIO.FALLING, callback=select_item4, bouncetime=200)
    GPIO.add_event_detect(BtnPin7, GPIO.FALLING, callback=backdir, bouncetime=200)
    while True:
        time.sleep(1)
        
def destroy():
    GPIO.cleanup()
    


#########################
# PRINT ITEMS ON SCREEN #
#########################

#establish root directory
rootdir = '/home/pi/Music'

# create class to navigate directories
class navfolders:
    def __init__(self):
        self.currentdir = rootdir
        self.list_index=0
        
    # method: print list of items
    def listitems(self,listqty):
        self.listqty=listqty

        # list folders in current directory
        listfolders=[]
        filenames = sorted(os.listdir(self.currentdir))
        for filename in filenames:
            if os.path.isdir(os.path.join(os.path.abspath(self.currentdir),filename)):
                listfolders.append(filename)
        
        # list files in current directory
        listfiles=[]
        for filename in filenames:
            if os.path.isfile(os.path.join(os.path.abspath(self.currentdir),filename)):
                listfiles.append(filename)
        
        # merge folders and files into one list
        self.mergelist = listfolders + listfiles


        currentitems=[]
        self.numlist = len(self.mergelist)   #find total number of items in directory
        
        # print onto screen (listqty) items at a time
        for x in range(self.listqty):
            if self.list_index<self.numlist:
                currentitems.append(self.mergelist[self.list_index])
                print self.mergelist[self.list_index]
                self.list_index+=1
            else:
                print ' '
                self.list_index+=1
            
        self.list_index=self.list_index-self.listqty # reset counter to first item in list
        
    # method: navigate through list
    def navigatelist(self,nav):
    
        if nav==1:  #navigate forward
            if self.list_index+self.listqty>=self.numlist:
                self.listitems(self.listqty)
            else:
                self.list_index+=self.listqty
                self.listitems(self.listqty)  # call list method to print items to screen

        elif nav==2:  #navigate backward
            self.list_index-=self.listqty
            if self.list_index < 0:
                self.list_index=0
            self.listitems(self.listqty)

        else:
            print 'your input got messed up'


#################
# START PROGRAM #
#################

#establish list of classes to be used for each file directory
directory=list()
for z in range(20):
    directory.append(z)

#first in list of classes is root file directory, list first items in root dir
i=0
directory[i]=navfolders()
directory[i].listitems(4)

# start program!
if __name__== '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

'''    
request=1
while request>0 and request<8:
    print '\n'
    request=input('Select: "1"-"4" or Navigate Forward="5" Back="6" or Back a directory "7"\n')
    
# print next 4 items in list   
    if request==5 or request==6:
        directory[i].navigatelist(request)


# select folder/file: if folder, run class for that directory path
#                     if file, run mplayer?
    elif request==1 or request==2 or request==3 or request==4:
        selection=os.path.join(os.path.abspath(directory[i].currentdir),directory[i].mergelist[directory[i].list_index+request-1])
        i+=1
        
        if os.path.isdir(selection):
            rootdir=selection
            directory[i]=navfolders()
            directory[i].listitems(4)
            
        elif os.path.isfile(selection):
            print  'this is file!!'
        
# navigate back one directory
    elif request==7:
        if i>0:
            i-=1
            directory[i].listitems(4)
        else: directory[i].listitems(4)
'''