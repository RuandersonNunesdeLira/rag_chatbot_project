import requests
from src.core import config

class EvolutionAPIClient():
    def __init__(self):
        self.api_url = config.EVOLUTION_API_URL
        self.api_key = config.EVOLUTION_API_KEY
        self.api_instance_name = config.EVOLUTION_INSTANCE_NAME

        self.url = f"http://{self.api_url}/message/sendText/{self.api_instance_name}"
        self.headers = {"apikey": self.api_key, "Content-Type": "application/json"}


    def send_message(self, message, phone_number):

        payload = {"number": phone_number, "textMessage": {"text": message}}

        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            print(f"API Status Code: {response.status_code}")
            print(f"API Response: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"ERRO ao conectar com a API de mensagens: {e}")
            return None




