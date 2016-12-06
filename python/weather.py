#do not like doing this, but this gives us an "old" way in python3
from six.moves import urllib
import json

url = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor="
page = urllib.request.urlopen(url)
data = page.read()
data2 = data.decode("UTF-8")

json_obj = json.loads(data2)

print(json_obj)
