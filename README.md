# seat
test tricking on WHU library seat booking system\n
数据格式：
座位：chrome审核元素查看座位号
日期：YYYY-MM-DD形式输入
时间：从0点起计算的分钟数 如8:30--8*60+30=510 17:00--17*60=1020
环境：Python 3.5.2 |Anaconda 4.0.0 (64-bit)
库：requests、pyqt4
打包工具：pyinstaller
打包文件：
http://pan.baidu.com/s/1dFdxqbZ 
使用方法:点击开始后，下方会提示结果，如果没有抢成功，将会提示失败原因，并在后台循环发送数据，直至成功
所以，应当在22点后将其打开并启动提交，放置一边即可，等待其自动完成抢座
