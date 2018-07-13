#!/usr/bin/env python
import LMK.GPIO as GPIO
import time
PIN_NUM=7
PIN_IN=10
val=0
GPIO.setmode(GPIO.BOARD)
while 1:
       try:
           GPIO.setup(PIN_NUM,GPIO.OUT)
	   GPIO.setup(PIN_IN,GPIO.IN)
       except:
           print("fail to setup GPIO %d",PIN_NUM)
       val=GPIO.input(PIN_IN)
       if val:
        GPIO.output(PIN_NUM,True)
       else :
        GPIO.output(PIN_NUM,False)
       
