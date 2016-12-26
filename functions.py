import requests
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
def get_start():
    s=requests.session()
    html = s.get('http://seat.lib.whu.edu.cn/simpleCaptcha/captcha',headers=s.headers)
    f = open('cookies.png', 'wb+')
    f.write(html.content)
    f.close()
    return s
def common_ui(self,x,y,width,lenth):
    palette1 = QPalette()
    palette1.setColor(self.backgroundRole(), QColor(255, 255, 255))
    self.setPalette(palette1)
    self.setGeometry(x, y, width, lenth)
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
    self.setWindowTitle('No.33')
def login(s,account,password,indentifier):
    response=s.post("http://seat.lib.whu.edu.cn/auth/signIn",data={"username":str(account),"password":str(password),"captcha":indentifier})
    return response
def booking(s,date,seat,start,end):
    response=s.post("http://seat.lib.whu.edu.cn/selfRes",data={"date":date,"seat":str(seat),"start":str(start),"end":str(end)})
    return response
def check(response):
    target = re.findall('<div class=\"content\">(.*?)</div>', response.text, re.S).pop()
    if('凭证号'in target):
        return 1,target
    elif('预约失败' in target):
        return 2,target
    else:
        return 0,target
def login_check(response):
    if('DOCTYPE' in response):
        return 0
    else:
        return 1