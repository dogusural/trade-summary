import hmac
import hashlib
import time
import requests
import json
import aes



try:
    with open('keys.json') as file:
        documents = json.load(file)
        encrypted_api_key= documents["exchanges"][0]['keys'][0]['api-key']
        encrypted_api_secret = documents["exchanges"][0]['keys'][1]['api-secret']
        key = input("Enter your password :").encode()
        key_sha256 = hashlib.sha256(key).digest()
        cipher = aes.AESCipher(key_sha256)
        api_key=cipher.decrypt(encrypted_api_key)
        api_secret=cipher.decrypt(encrypted_api_secret)


except IOError:
    print("keys.json doesn't exist. Creating the file ...")
    with open('keys.json',"w") as file:
        api_key = input("Enter your API-key :")
        api_secret = input("Enter your API-secret :")
        key = input("Enter your password :").encode()
        key_sha256 = hashlib.sha256(key).digest()
        cipher = aes.AESCipher(key_sha256)
        data = {}
        data['exchanges'] = []
        data['exchanges'].append({
            'name': 'Binance',
            'website': 'binance.com',
            'keys': [{"api-key":str(cipher.encrypt(api_key).decode())},{"api-secret":str(cipher.encrypt(api_secret).decode())}]
        })
        data = json.dump(data, file)




BASE_URL="https://api.binance.com/"
API_URL="api/v3/myTrades"

PAIR="ETHUSDT"
TIMESTAMP=int(round(time.time() * 1000))
AVAX_BODY="symbol="+PAIR+"&recvWindow=60000&timestamp="+str(TIMESTAMP)




signature = hmac.new(api_secret.encode(), AVAX_BODY.encode(), hashlib.sha256).hexdigest()

BODY=BASE_URL+API_URL+"?"+AVAX_BODY+"&signature="+signature


x = requests.get(BODY, headers = {"X-MBX-APIKEY": api_key})

json_object = json.loads(x.text)

json_formatted_str = json.dumps(json_object,sort_keys=True, indent=2)

print(json_formatted_str)


