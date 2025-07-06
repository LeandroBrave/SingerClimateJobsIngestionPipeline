import requests
from urllib.parse import urlencode

#Essa classe é responsável por fazer as requisições e retornar as respostas

class RequestsClient:

    def __init__(self, base_url, endpoint, params):
        """
        base_url: string, ex: https://api.open-meteo.com
        endpoint: string, ex.: 'v1/forecast'
        params: dict com os query parameters
        """
        self.base_url = base_url
        self.endpoint = endpoint
        self.params = params

    def get(self):
        url = f"{self.base_url}/{self.endpoint}"
        
        # Para debug, mostra a URL completa:
        query_string = urlencode(self.params)
        full_url = f"{url}?{query_string}"
        print(f"Full URL: {full_url}")

        response = requests.get(url, params=self.params)
        response.raise_for_status()
        return response.json()
