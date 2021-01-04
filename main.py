import hmac
import hashlib
import time
import requests
import json
import configs



setup = configs.setup()


API_URL="api/v3/myTrades"

PAIR="ETHUSDT"
TIMESTAMP=int(round(time.time() * 1000))
AVAX_BODY="symbol="+PAIR+"&recvWindow=60000&timestamp="+str(TIMESTAMP)




signature = hmac.new(setup.get_api_secret().encode(), AVAX_BODY.encode(), hashlib.sha256).hexdigest()

BODY=setup.get_api_url()+API_URL+"?"+AVAX_BODY+"&signature="+signature


x = requests.get(BODY, headers = {"X-MBX-APIKEY": setup.get_api_key()})

json_object = json.loads(x.text)

json_formatted_str = json.dumps(json_object,sort_keys=True, indent=2)

print(json_formatted_str)


