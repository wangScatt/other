#coding:utf-8

import threading
import socket
import json
import hashlib
import time

Server_IP = "www.bigiot.net"
Server_Port = 8282

class Device:
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.reciver_thread = threading.Thread(target=self.reciver_loop,args=())
		self.reciver_thread.setDaemon(True)
		self.ID = None
		self.Busy = False
		self.__ret_data__ = None
		self.connect()

#Connect Server
	def connect(self):
		try:
			self.socket.connect((Server_IP,Server_Port))
		except socket.error,e:
			print "Error connect: %s"%(e)
			exit(1)
		self.reciver_thread.start()
		return "OK"

#Send data, and wait for a return
	def socket_send(self,str):
		self.Busy = True
		self.socket.send(str)
		start_time = time.time()
		while self.Busy:
			time.sleep(0.1)
			if time.time()-start_time > 1:
				return None
		return json.loads(""+self.__ret_data__)

#Receive data callback 
	def tcp_recv_callback(self,ret):
		#print ret
		pass

#Sockets receive data
	def reciver_loop(self):
		while True:
			res =  self.socket.recv(1024)
			self.tcp_recv_callback(res[:-1])
			res = json.loads(res)
			M = res["M"]
			
			if M == "b":
				self.socket.send('{"M":"status"}\n')
				continue
			elif M == "WELCOME TO BIGIOT":
				continue
			elif M == "checkinok":
				self.ID = res["ID"]
			elif M == "login":
				self.login_callback(res)
				continue
			elif M == "logout":
				self.logout_callback(res)
				continue
			elif M == "say":
				self.say_callback(res)
				continue
				
			if self.Busy == True:
				if M != "say":
					self.__ret_data__ = json.dumps(res)
					self.Busy = False

#Device login
	def checkin(self,ID,K,Token=None):
		if Token <> None:
			md5_obj = hashlib.md5()
			md5_obj.update(Token+K)
			K = md5_obj.hexdigest()
			#print "Safe_login %s"%K
		self.ID = ID
		obj = {"M":"checkin","ID":ID,"K":K}
		obj = json.dumps(obj)+"\n"
		#print obj
		return self.socket_send(obj)

#User and device on-line notification data
	def login_callback(self,ret):
		pass

#User or device off-line notification data
	def logout_callback(self,ret):
		pass

#Someone triggers a callback function when you talk to you
	def say_callback(self,ret):
		pass

#Speak to other people
	def say(self,ID,C,SIGN):
		obj = {"M":"say","ID":ID,"C":C,"SIGN":SIGN}
		obj = json.dumps(obj)+"\n"
		self.socket.send(obj)

#Check online
	def isOL(self,ID):
		obj = {"M":"isOL","ID":ID}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

#Get the device status
	def status(self):
		obj = {"M":"status"}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

#Send an alert
	def alert(self,C,B):
		obj = {"M":"alert","C":C,"B":B}
		obj = json.dumps(obj)+"\n"
		self.socket.send(obj)

#Get the server time
	def time(self,F="stamp"):
		obj = {"M":"time","F":F}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

#Forced to log out
	def checkinout(self,ID,K):
		obj = {"M":"checkout","ID":ID,"K":K}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

#Submit data to the data interface
	def update(self,data):
		obj = {"M":"update","ID":self.ID[1:],"V":data}
		obj = json.dumps(obj)+"\n"
		#print obj[:-1]
		self.socket.send(obj)
