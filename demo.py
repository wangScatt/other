import urllib2
import json
req = urllib2.Request('https://api.seniverse.com/v3/weather/now.json?key=9rrrxbzk7fszhrir&location=shenzhen&language=en&unit=c')
res = urllib2.urlopen(req)

data = json.loads(res.read())


print data['results'][0]['now']['text']


res.close()
