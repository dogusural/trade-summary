import aes
import json
import hashlib

class setup():
    def __init__(self) :
        try:
            with open('keys.json') as file:
                documents = json.load(file)
                print("keys.json found. Proceeding ...")
                encrypted_api_key= documents["exchanges"][0]['keys'][0]['api-key']
                encrypted_api_secret = documents["exchanges"][0]['keys'][1]['api-secret']
                self.base_url = documents["exchanges"][0]["api-url"]
                key = input("Enter your password :").encode()
                key_sha256 = hashlib.sha256(key).digest()
                cipher = aes.AESCipher(key_sha256)
                self.api_key=cipher.decrypt(encrypted_api_key)
                self.api_secret=cipher.decrypt(encrypted_api_secret)

        except IOError:
            print("keys.json doesn't exist. Creating the file ...")
            with open('keys.json',"w") as file:
                self.api_key = input("Enter your API-key :")
                self.api_secret = input("Enter your API-secret :")
                self.base_url = 'https://api.binance.com/'
                key = input("Enter your password :").encode()
                key_sha256 = hashlib.sha256(key).digest()
                cipher = aes.AESCipher(key_sha256)
                data = {}
                data['exchanges'] = []
                data['exchanges'].append({
                    'name': 'Binance',
                    'website': 'binance.com',
                    'api-url' : self.base_url,
                    'keys': [{"api-key":str(cipher.encrypt(api_key).decode())},{"api-secret":str(cipher.encrypt(api_secret).decode())}]
                })
                data = json.dump(data, file)

        except KeyError:
            print("There seems to be an error within the \"keys.json\" file. Terminating the program ...")
            exit()
    def get_api_key(self):
        return self.api_key
    def get_api_secret(self):
        return self.api_secret
    def get_api_url(self):
        return self.base_url
