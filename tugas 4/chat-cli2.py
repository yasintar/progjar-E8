import socket
import os
import json

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889


class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""

    def proses(self,cmdline):
        j=cmdline.split(" ")
        try:
            command=j[0].strip()
            if (command=='auth'):
                username=j[1].strip()
                password=j[2].strip()
                return self.login(username,password)
            elif (command=='send'):
                usernameto = j[1].strip()
                message=""
                for w in j[2:]:
                    message="{} {}" . format(message,w)
                return self.sendmessage(usernameto,message)
            elif (command=='inbox'):
                return self.inbox()
            elif (command == 'logout'):
                return self.logout()
            elif (command == 'create_group'):
                group = j[1].strip()
                return self.create_group(group)
            elif (command == 'join_group'):
                group = j[1].strip()
                return self.join_group(group)
            elif (command == 'leave_group'):
                group = j[1].strip()
                return self.leave_group(group)
            elif (command == 'send_group'):
                group = j[1].strip()
                message = ""
                for w in j[2:]:
                    message = "{} {}".format(message, w)
                return self.sendmessage_group(group, message)
            elif (command == 'inbox_group'):
                group = j[1].strip()
                return self.inbox_group(group)
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"

    def sendstring(self,string):
        try:
            self.sock.sendall(string)
            receivemsg = ""
            while True:
                data = self.sock.recv(10)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data)
                    if receivemsg[-4:]=="\r\n\r\n":
                        return json.loads(receivemsg)
        except:
            self.sock.close()

    def login(self,username,password):
        string="auth {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return "username {} logged in, token {} " .format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])

    def logout(self):
        if (self.tokenid == ""):
            return "Your're not logged in."
        string = "logout {} \r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            # print self.tokenid
            self.tokenid = ""
            return "Successfully logged out."
        else:
            return "500 Internal server error."

    def sendmessage(self,usernameto="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])
    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])

    def create_group(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "create_group {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def join_group(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "join_group {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def leave_group(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "leave_group {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def sendmessage_group(self, group_name, message):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "send_group {} {} {} \r\n".format(group_name, self.tokenid, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def inbox_group(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "inbox_group {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['messages']))
        else:
            return "Error, {}".format(result['message'])

if __name__=="__main__":
    cc = ChatClient()
    while True:
        cmdline = raw_input("Command {}:" . format(cc.tokenid))
        print cc.proses(cmdline)

