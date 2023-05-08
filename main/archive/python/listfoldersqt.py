# list files/folders (listqty) at a time, buttons select/navigate
import os
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

#pyqt GUI setup class
class Example (QWidget):
    def __init__(self):
        super(Example,self).__init__()
        self.initUI()
        
    def initUI(self):
        
        lbl1=QLabel(directory[i].mergelist[directory[i].i_place],self)
        lbl1.move(15,10)
        
        lbl2=QLabel(directory[i].mergelist[directory[i].i_place+1],self)
        lbl2.move(15,40)
        
        lbl3=QLabel(directory[i].mergelist[directory[i].i_place+2],self)
        lbl3.move(15,70)

        lbl3=QLabel(directory[i].mergelist[directory[i].i_place+3],self)
        lbl3.move(15,100)
        
        qbtn=QPushButton('GIT!',self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150,50)
        
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('PiRadio')
        self.show()
        


#establish root directory
rootdir = '/home/pi/Music'

# create class to navigate directories
class navfolders:
    def __init__(self):
        self.currentdir = rootdir
        self.i_place = 0
        
    # method show list of items
    def listitems(self, listqty):
        self.listqty = listqty
        
        # create merged list of folders and files that are in current directory
        listfolders=[]
        filenames = sorted(os.listdir(self.currentdir))
        for filename in filenames:
            if os.path.isdir(os.path.join(os.path.abspath(self.currentdir),filename)):
                listfolders.append(filename)
        
        listfiles=[]
        for filename in filenames:
            if os.path.isfile(os.path.join(os.path.abspath(self.currentdir),filename)):
                listfiles.append(filename)
                
        self.mergelist = listfolders + listfiles


        # print onto screen [listqty] items at a time
        currentitems=[]
        self.numlist = len(self.mergelist)   #establish total number of items in directory
        
        for x in range(listqty):
            if self.i_place<self.numlist:
                currentitems.append(self.mergelist[self.i_place])
                print self.mergelist[self.i_place]
                self.i_place+=1
            else:
                print ' '
                self.i_place+=1
            
        self.i_place=self.i_place-listqty # reset counter to first item in list
        
    # method: navigate through list
    def navigatelist(self,nav):
    
        if nav==5:
            if self.i_place+self.listqty>=self.numlist:
                self.listitems(self.listqty)
            else:
                self.i_place+=self.listqty
                self.listitems(self.listqty)  # call list method to print items to screen

        elif nav==6:
            self.i_place-=self.listqty
            if self.i_place < 0:
                self.i_place=0
            self.listitems(self.listqty)

        else:
            print 'your input got messed up'


##################
"""Script below"""
##################

#establish list of classes to be used for each file directory
directory=list()
for i in range(20):
    directory.append(i)

#list first items in root dir
i=0
directory[i]=navfolders()
directory[i].listitems(4)

'''
request=1 #Make =0 in order to negate
while request>0 and request<8:
    print '\n'
    request=input('Select: "1"-"4" or Navigate Forward="5" Back="6" or Back a directory "7"\n')
    
# print next 4 items in list   
    if request==5 or request==6:
        directory[i].navigatelist(request)


# select folder/file: if folder, run class for that directory path
#                     if file, run mplayer?
    elif request==1 or request==2 or request==3 or request==4:
        selection=os.path.join(os.path.abspath(directory[i].currentdir),directory[i].mergelist[directory[i].i_place+request-1])
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
        
# execute pyqt GUI class
if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())
