#pyqt GUI setup class
class mainView (QWidget):
    def __init__(self):
        super(mainView,self).__init__()
        self.initUI()
        
    def initUI(self):
        
        btn1=QPushButton('SD',self)
        btn1.move(15,10)
        btn1.clicked.connect(callBtn1)
        btn1.clicked.connect(self.on_button)
        
        btn2=QPushButton('Bluetooth',self)
        btn2.move(15,40)
        btn2.clicked.connect(callBtn2)
        
        btn3=QPushButton('FM radio',self)
        btn3.move(15,70)
        btn3.clicked.connect(callBtn3)

        btn4=QPushButton('AUX',self)
        btn4.move(15,100)
        btn4.clicked.connect(callBtn4)
        
        qbtn=QPushButton('GIT!',self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150,50)
        
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('PiRadio')
        self.show()
        
    def on_button(self):
        self.dialog=sdView()
        self.dialog.show()

