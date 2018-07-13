# A Simple BigIoT SDK for Python
这是这个SDK的详细使用方法

## connect()
* 返回：无返回
* 参数：无参数
* 用途：用于连接服务器，当Device类实例化时，会自动连接，但不自动登录。
```python
a = Device()
a.connect()
```

## checkin(ID,K,Token)
* 返回： Dict类型，参照API官方文档，第1项，例如：
  ``` {"M":"checkinok","ID":"xx1","NAME":"xx2","T":"xx3"}\n ```
* 参数：ID---设备ID，K---设备API-Key，Token---设备的Token，当进行一次普通登陆后，可获取一枚Token，用于进行MD5加密登录
* 用途：用于登录服务器。
  * 设备登录后，如果在1分钟内无数据传送，连接将被自动关闭.
  * 登录失败反回 `None`

普通登录
```python
a.checkin("设备ID","设备API-Key")
```
加密登录
```
token = a.checkin("设备ID","设备API-Key") #得到Token
a.checkin("设备ID","用户API-Key",token) #加密登陆，token和API-Key加密
```
## isOL(ID)
* 返回：Dict类型，参照API官方文档,第6项，例如：
  ``` {"M":"isOL","R":{"XX1":"xx1",...},"T"":"xx3"}\n ```
* 参数：ID---设备ID，支持多个查询``` ["ID1","ID2"......] ```
* 用途：查询设备或用户是否在线
```python
print a.isOL("Dxx")
```

## status()
* 返回： Dict类型，参照API官方文档,第7项
* 参数：无参数
* 用途：查询当前设备状态

## time()
* 返回：Dict类型，参照API官方文档,第9项
* 参数：用于选择时间格式，默认stamp
  * stamp返回：1466659300
    * Y-m-d返回：2016-06-21
    * Y.m.d返回：2016.06.21
    * Y-m-d H:i:s返回：2016-06-21 10:25:30
* 用途：查询服务器时间

## checkinout（ID,K)
* 返回：参照官方第10项目
* 参数：
	* ID：目标设备ID
	* K：目标设备API-key
* 用途：强制目标设备下线

## say(ID,C,SIGN)
* 返回：参照官方第5项
* 参数：
	* ID：目标设备ID
	* C：具体消息
	* SIGN：签名
* 用途：向其他设备或用户发送数据

## alert(C,B)
* 返回：无返回
* 参数：
	* C：报警内容
	* B：报警方式，支持email、weibo、qq
* 用途：发送报警信息

## update(data)
* 返回：无返回，参照官方第2项
* 参数：dict类型，以接口ID作为键值
* 用途：向数据接口提交数据

下面介绍带有callback的函数
---
## login_callback(ret)
用途：用户和设备上线通知数据

## logout_callback(ret)
用途：用户和设备下线通知数据
以上两个参照官方第3项和第4项，ret参数为其套接字接收到的数据
```python
def f_in(ret):
	print "login %s"%ret["NAME"]

def f_out(ret):
	print "logout %s"%ret["NAME"]

a.login_callback = f_in
a.logout_callback = f_out
# 接下来，当上线或下线的时候，会触发f_in和f_out
```

## say_callback(ret)
用途：当别人向这个设备发送消息的时候，会触发这个函数
使用方法类上，参数参照官方第5项
