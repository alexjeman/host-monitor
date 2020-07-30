import requests


class APIHandler:
    def __init__(self, obj, chat_id, api_url="https://hostmonitor.curs-valutar.xyz/"):
        self.chat_id = chat_id
        self.api_url = api_url
        self.obj = obj

    def get_apikey_info(self):
        my_key = self.obj.query.filter_by(chat_id=self.chat_id).first()
        response = requests.get(f"{self.api_url}apikey/{my_key.key}")
        return response


class APIHandlerNew:
    def __init__(self, chat_id, api_url="https://hostmonitor.curs-valutar.xyz/"):
        self.chat_id = chat_id
        self.api_url = api_url

    def get_newkey(self):
        body = {"email": f"{self.chat_id}"}
        response = requests.post(self.api_url + "apikey/", json=body)
        return response
