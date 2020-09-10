import telnetlib
import time

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from app.telnetConfig import telnetConfig
import socket

import traceback





class telnetTube(object):

    def __init__(self,config:telnetConfig):# telnettube和config：关联关系
        self.telnet = telnetlib.Telnet()
        self.is_open = False
        self.config=config


    def open(self) -> bool:
        self.close()
        errarg = [f"无法连接设备", f"host:{self.config.host}",f"port:{self.config.port}"]
        self.telnet.host = self.config.host
        self.telnet.port = self.config.port
        self.telnet.timeout = self.config.timeout
        try:
            self.telnet.open(self.telnet.host,self.telnet.port)

            errarg.append(f"username:{self.config.username}")
            errarg.append(f"password:{self.config.password}")

            self.telnet.read_until(b'login:')
            self.telnet.write(self.config.username.encode('utf-8')+b"\n")

            self.telnet.read_until(b'Password:')
            self.telnet.write(self.config.password.encode('utf-8')+b"\n")

            time.sleep(3)
            respond=self.telnet.read_very_eager().decode('utf-8')
            while not respond:
                respond = self.telnet.read_very_eager().decode('utf-8')
            print(respond)
            if 'Login incorrect' in respond:
                    raise ValueError()
            self.is_open = True
        except socket.timeout:
            raise Exception(errarg,"提示：连接超时")
        except ValueError:
            raise Exception(errarg,"提示：用户名或密码错误")
        except:

            traceback.print_exc()
            raise Exception(errarg,"提示：请确保 Telnet 配置正确，设备正常运行且线路正常连接。")

        return self.is_open

    def close(self) -> bool:
        self.telnet.close()
        self.is_open = False
        return self.is_open

    def send(self,command,devdata):# telnetTube和data:依赖关系
        # command=devdata.send
        # devdata.devicename=self.config.host
        devdata.sendtop=False
        devdata.sendfree=False
        devdata.sendinvalid=False
        try:
            if(command=="free"):
                devdata.sendfree=True
            elif command=="top":
                devdata.sendtop=True
            else:
                devdata.sendinvalid=True

            self.telnet.write(command.encode('utf-8')+b'\n')
        except Exception as e:
            raise Exception("send数据到主机失败",f"host:{self.config.host}",f"port:{self.config.port}")

    def receive(self,devdata):
        result=''
        try:
            while not result:
                time.sleep(1)
                result=result+self.telnet.read_very_eager().decode('utf-8')
            result= ILLEGAL_CHARACTERS_RE.sub(r'', result)
            print(result)
            print("接收到了")
            if devdata.sendfree==True:
                devdata.receivefree.append((self.config.host,result))
                print(devdata.receivefree)
            else:
                devdata.receivetop.append((self.config.host,result))
                print(devdata.receivetop)
        except Exception:
            traceback.print_exc()
            raise Exception("从目标receive数据失败",f"host:{self.config.host}",f"port:{self.config.port}")