import threading
import socket
import json
import hashlib
import time
import urllib2

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

a = Device()
qobj = {"M":"checkin","ID":"4571","K":"f8c387a33"}
qobj = json.dumps(qobj)+"\n"
a.socket_send(qobj)
time.sleep(5)
while(1):
        
 req = urllib2.Request('https://api.seniverse.com/v3/weather/daily.json?key=9rrrxbzk7fszhrir&location=shenzhen&language=en&unit=c&start=0&days=5')
 res = urllib2.urlopen(req)
 data = json.loads(res.read())
 time.sleep(10)
 req = urllib2.Request('https://api.seniverse.com/v3/weather/now.json?key=9rrrxbzk7fszhrir&location=shenzhen&language=en&unit=c')
 res = urllib2.urlopen(req)
 data_now = json.loads(res.read())


 for i in range(1,60):

  qobj = {"M":"say","ID":"ALL","C":"wo"}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp = str(data_now['results'][0]['now']['temperature'])
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp = str(data_now['results'][0]['now']['text'])
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  #ppp = str(data['results'][0]['daily'][0]['date'])
  ppp = time.strftime('%Y-%m-%d',time.localtime(time.time()))
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  
  qobj = {"M":"say","ID":"ALL","C":"xi"}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp = str(data['results'][0]['daily'][0]['date']) + "    " + str(data['results'][0]['daily'][0]['low']) + "~" + str(data['results'][0]['daily'][0]['high'])
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp = "day  :" +  str(data['results'][0]['daily'][0]['text_day']);
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp ="night:" + str(data['results'][0]['daily'][0]['text_night'])
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)

  qobj = {"M":"say","ID":"ALL","C":"huan"}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp = str(data['results'][0]['daily'][1]['date']) + "    " + str(data['results'][0]['daily'][1]['low']) + "~" + str(data['results'][0]['daily'][1]['high'])
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp = "day  :" +  str(data['results'][0]['daily'][1]['text_day']);
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)
  ppp ="night:" + str(data['results'][0]['daily'][1]['text_night'])
  qobj = {"M":"say","ID":"ALL","C":ppp}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(15)

  qobj = {"M":"say","ID":"ALL","C":"ni"}
  qobj = json.dumps(qobj)+"\n"
  a.socket_send(qobj)
  time.sleep(40)
