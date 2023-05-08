import time
import os
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

def get_colors():
    randnums=[]
    neg_randnums=[]
    for x in range(3):
        z=random.randint(0,2)
        randnums.append(z)
        if z==0: neg_randnums.append(2)
        elif z==1: neg_randnums.append(z)
        elif z==2: neg_randnums.append(0)

    len_nums=len(randnums)
    colors=[]
    neg_colors=[]
    for x in range(len_nums):
        colors.append(127*randnums[x])
        neg_colors.append(127*neg_randnums[x])

    print colors
    print neg_colors
    
get_colors()


#pyqt GUI setup class
class mainView (QWidget):
    def __init__(self):
        super(mainView,self).__init__()
        self.initUI()
        
    def initUI(self):

        #set colors for buttons
        randnums=[]
        neg_randnums=[]
        for x in range(3):
            z=random.randint(0,2)
            randnums.append(z)
            if z==0: neg_randnums.append(2)
            elif z==1: neg_randnums.append(z)
            elif z==2: neg_randnums.append(0)

        len_nums=len(randnums)
        colors=[]
        neg_colors=[]
        for x in range(len_nums):
            colors.append(127*randnums[x])
            neg_colors.append(127*neg_randnums[x])

        
        #define buttons
        btn1 = QPushButton('SD',self)
        btn1.move(15,10)
        btn1.setStyleSheet("color:rgb(%d,%d,%d)" %(colors[0],colors[1],colors[2]))
        
        btn2 = QPushButton('Bluetooth',self)
        btn2.move(15,40)
        btn2.setStyleSheet("color:blue")
        
        btn3 = QPushButton('FM radio',self)
        btn3.move(15,70)
        btn3.setStyleSheet("color:green")

        btn4 = QPushButton('AUX',self)
        btn4.move(15,100)
        btn4.setStyleSheet("color:purple")
        
        qbtn=QPushButton('GIT!',self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150,50)

        
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('PiRadio')
        self.show()

# start program!
if __name__== '__main__':
    app=QApplication(sys.argv)
    window1=mainView()
    sys.exit(app.exec_())

      
