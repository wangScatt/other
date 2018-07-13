import time

print time.time()

time.localtime(time.time())

timeNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
print timeNow
