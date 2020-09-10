# -*- encoding: utf-8 -*-
import time

from app.devData import devData
from app.telnet import telnetTube
from app.telnetConfig import telnetConfig
import xlwt
host=""
configlist=[]
count=1
while True:
    print("输入q停止添加设备")
    print("第%d个设备：" % count)
    host=input("输入host:")
    if host=='q':
        break
    port=input("输入端口：")
    username = input("输入用户名：")
    passport = input("输入密码：")
    count=count+1
    print()
    configlist.append((host,port,username,passport))

# configlist=configlist[0:len(configlist)-1]
print(configlist)
devdata=devData()
try:
    devdata.createxel()
except Exception as err:
    print(err)


for item in configlist:
    config=telnetConfig(item[0],item[2],item[3],item[1])
    telnettube=telnetTube(config)
    if telnettube.is_open==False:
        try:
            telnettube.open()
            print("open 完成")


            try:
                telnettube.send("free", devdata)
                while devdata.sendinvalid==True:
                    telnettube.send("free",devdata)
                print("send free完成")

                telnettube.receive(devdata)
                print("receive完成")
            except Exception as err:
                print(err)
            try:
                telnettube.send("top", devdata)
                while devdata.sendinvalid == True:
                    telnettube.send("top",devdata)
                print("send top完成")
                telnettube.receive(devdata)
                print("receive完成")
            except Exception as err:
                print(err)

            telnettube.close()
            print("close完成")
        except Exception as err:
            print(err)
devdata.combine()

try:
    devdata.addtoexcel()
except Exception as err:
    print(err)