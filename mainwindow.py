import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import requests
import functions
import booking
import tkinter
class MainWindow(QDialog):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        functions.common_ui(self,100,500,300,250)
        self.session=functions.get_start()
        self.layout=QVBoxLayout()

        self.AccountLine = QLineEdit()
        self.AccountLine.setFixedHeight(27)
        self.AccountLine.setFixedWidth(200)
        self.account_lable=QLabel("账户")
        self.account_lable.setAlignment(Qt.AlignCenter)
        self.account_lable.setFont(QFont("Microsoft YaHei",20))
        self.account_layout=QHBoxLayout()
        self.account_layout.addWidget(self.account_lable)
        self.account_layout.addWidget(self.AccountLine)

        self.PassWord = QLineEdit()
        self.PassWord.setFixedHeight(27)
        self.PassWord.setFixedWidth(200)
        self.PassWord.setEchoMode(QLineEdit.Password)
        self.PassWord_lable = QLabel("密码")
        self.PassWord_lable.setAlignment(Qt.AlignCenter)
        self.PassWord_lable.setFont(QFont("Microsoft YaHei", 20))
        self.PassWord_layout = QHBoxLayout()
        self.PassWord_layout.addWidget(self.PassWord_lable)
        self.PassWord_layout.addWidget(self.PassWord)

        self.identify = QLineEdit()
        self.identify.setFixedHeight(27)
        self.identify.setFixedWidth(100)
        self.identify_lable = QLabel("验证码")
        self.identify_lable.setAlignment(Qt.AlignCenter)
        self.identify_lable.setFont(QFont("Microsoft YaHei", 20))
        self.identify_pic=QLabel()
        self.pic=QPixmap("cookies.png")
        martix = QMatrix()
        martix.scale(0.6, 0.6)
        self.identify_pic.setPixmap(self.pic.transformed(martix))
        self.identify_layout = QHBoxLayout()
        self.identify_layout.addWidget(self.identify_lable)
        self.identify_layout.addWidget(self.identify)
        self.identify_layout.addWidget(self.identify_pic)


        self.save_account=QCheckBox("保存账户")
        self.save_account.setFont(QFont("Microsoft YaHei",10))

        self.save_password=QCheckBox("保存密码")
        self.save_password.setFont(QFont("Microsoft YaHei", 10))
        self.save_layout=QHBoxLayout()
        self.save_layout.addWidget(self.save_account)
        self.save_layout.addWidget(self.save_password)

        self.confirm_button = QPushButton()
        self.confirm_button.setText("起飞！")
        self.confirm_button.setFont(QFont("Microsoft YaHei", 20))

        self.info_lable=QLabel()

        self.layout.addLayout(self.account_layout)
        self.layout.addLayout(self.PassWord_layout)
        self.layout.addLayout(self.save_layout)
        self.layout.addLayout(self.identify_layout)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.info_lable)

        self.layout.addStretch()
        self.setLayout(self.layout)
        self.load_info()
        self.connect(self.save_password,SIGNAL("clicked()"),self.syn_info)
        self.connect(self.confirm_button,SIGNAL("clicked()"),self.login)
    def login(self):
        response=functions.login(self.session,self.AccountLine.text(),self.PassWord.text(),self.identify.text())
        if(functions.login_check(response.text)):
            print("success")
            #print(response.text)
            if(self.save_password.checkState()):
                dic={'save_mode':2,'account':self.AccountLine.text(),'password':self.PassWord.text()}
            elif(self.save_account.checkState()):
                dic={'save_mode':1,'account':self.AccountLine.text(),'password':''}
            else:
                dic={'save_mode':0,'account':'','password':''}
            f=open('info','w')
            f.write(str(dic))
            f.close()
            self.booking=booking.Booking(self,self.session)
            self.booking.show()
            self.hide()
        else:
            self.session=functions.get_start()
            self.pic = QPixmap("cookies.png")
            martix = QMatrix()
            martix.scale(0.6, 0.6)
            self.identify_pic.setPixmap(self.pic.transformed(martix))
            print('failed')
            self.identify.setText('')
    def syn_info(self):
        if self.save_password.checkState():
            self.save_account.setChecked(True)
    def load_info(self):
        info=open("info","r")
        dic=eval(info.readline())
        if(dic["save_mode"]==1):
            self.AccountLine.setText(dic["account"])
            self.save_account.setChecked(True)
        elif(dic["save_mode"]==2):
            self.AccountLine.setText(dic["account"])
            self.save_account.setChecked(True)
            self.PassWord.setText(dic["password"])
            self.save_password.setChecked(True)
        info.close()
app = QApplication(sys.argv)
form =MainWindow()
form.show()
app.exec_()