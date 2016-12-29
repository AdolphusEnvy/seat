import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import functions
import datetime
class post_thread(QThread):
    signal = pyqtSignal(int,str)
    def __init__(self,parent=None,session=None,dic=None):
        super(post_thread,self).__init__(parent)
        self.session=session
        self.dic=dic
    def run(self):
        response = functions.booking(s=self.session, date=self.dic['date'], seat=self.dic['seat'],
                                     start=self.dic['start'], end=self.dic['end'])
        state, target = functions.check(response)
        self.signal.emit(state,target)
        while(1):
            response = functions.booking(s=self.session, date=self.dic['date'], seat=self.dic['seat'],
                                         start=self.dic['start'], end=self.dic['end'])
            state, target = functions.check(response)
            if(state==1):
                self.signal.emit(state,target)
                break
class Booking(QDialog):
    def __init__(self,parent=None,session=None,id=None):
        super(Booking,self).__init__(parent)
        #functions.common_ui(self,100,500,300,250)
        self.session=session
        self.id=id

        self.layout = QVBoxLayout()
        self.DateLine =QComboBox()
        self.DateLine.addItems([datetime.date.today().strftime("%Y-%m-%d"),(datetime.date.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")])
        self.DateLine.setFixedHeight(27)
        self.DateLine.setFixedWidth(200)
        self.Date_lable = QLabel("时间")
        self.Date_lable.setAlignment(Qt.AlignCenter)
        self.Date_lable.setFont(QFont("Microsoft YaHei", 20))
        self.Date_layout = QHBoxLayout()
        self.Date_layout.addWidget(self.Date_lable)
        self.Date_layout.addWidget(self.DateLine)

        self.layout = QVBoxLayout()
        self.SeatLine = QLineEdit()
        self.SeatLine.setFixedHeight(27)
        self.SeatLine.setFixedWidth(200)
        self.Seat_lable = QLabel("座位号")
        self.Seat_lable.setAlignment(Qt.AlignCenter)
        self.Seat_lable.setFont(QFont("Microsoft YaHei", 20))
        self.Seat_layout = QHBoxLayout()
        self.Seat_layout.addWidget(self.Seat_lable)
        self.Seat_layout.addWidget(self.SeatLine)

        self.StartLine = QLineEdit()
        self.StartLine.setFixedHeight(27)
        self.StartLine.setFixedWidth(200)
        self.Start_lable = QLabel("开始时间")
        self.Start_lable.setAlignment(Qt.AlignCenter)
        self.Start_lable.setFont(QFont("Microsoft YaHei", 20))
        self.Start_layout = QHBoxLayout()
        self.Start_layout.addWidget(self.Start_lable)
        self.Start_layout.addWidget(self.StartLine)

        self.EndLine = QLineEdit()
        self.EndLine.setFixedHeight(27)
        self.EndLine.setFixedWidth(200)
        self.End_lable = QLabel("结束时间")
        self.End_lable.setAlignment(Qt.AlignCenter)
        self.End_lable.setFont(QFont("Microsoft YaHei", 20))
        self.End_layout = QHBoxLayout()
        self.End_layout.addWidget(self.End_lable)
        self.End_layout.addWidget(self.EndLine)

        self.confirm_button = QPushButton()
        self.confirm_button.setText("开始")
        self.confirm_button.setFont(QFont("Microsoft YaHei", 20))

        self.info_lable = QLabel('''请用chrome审核元素找到你需要的座位的座位，时间为从0点开始的分钟数，如9:30=9*60+30=510,17:00=17*60=1020''')

        self.layout.addLayout(self.Date_layout)
        self.layout.addLayout(self.Seat_layout)
        self.layout.addLayout(self.Start_layout)
        self.layout.addLayout(self.End_layout)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.info_lable)
        self.setLayout(self.layout)
        functions.common_ui(self, 100, 500, 300, 250)
        self.load_used_seat()
        #self.DateLine.setText(time.strftime("%Y-%m-%d")[:-2])
        self.connect(self.confirm_button,SIGNAL('clicked()'),self.post)
        self.connect(self.confirm_button,SIGNAL("clicked()"),self.save_used_seat)
    def post(self):
        self.confirm_button.setDisabled(True)
        dic={'date':self.DateLine.currentText(),"seat":self.SeatLine.text(),"start":self.StartLine.text(),'end':self.EndLine.text()}
        print(dic)
        self.PostThread=post_thread(self,session=self.session,dic=dic)
        self.PostThread.signal.connect(self.info)
        #self.connect(self.PostThread.signal,SIGNAL('signal(int,str)'),self.info)
        self.PostThread.start()
    def info(self,state,target):
        if(state==1):
            self.info_lable.setText(target)
        else:
            self.info_lable.setText(target+'正在循环')
        self.confirm_button.setDisabled(False)
    def load_used_seat(self):
        f=open("used_seat","r")
        self.used_seat=eval(f.read())
        if(self.id in self.used_seat):
            self.SeatLine.setText(self.used_seat[self.id]['seat'])
            self.StartLine.setText(self.used_seat[self.id]['start'])
            self.EndLine.setText(self.used_seat[self.id]['end'])
        f.close()
    def save_used_seat(self):
        f=open("used_seat",'w')
        if(self.id in self.used_seat):
            self.used_seat[self.id]["seat"]=self.SeatLine.text()
            self.used_seat[self.id]["start"] = self.StartLine.text()
            self.used_seat[self.id]["end"] = self.EndLine.text()
        else:
            self.used_seat[self.id]={"seat":self.SeatLine.text(),"start":self.StartLine.text(),"end":self.EndLine.text()}
        f.write(str(self.used_seat))
        f.close()