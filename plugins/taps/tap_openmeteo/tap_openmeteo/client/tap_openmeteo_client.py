import requests
from urllib.parse import urlencode

#Essa classe é responsável por fazer as requisições e retornar as respostas

class TapOpenMeteoClient:
    BASE_URL = "https://api.open-meteo.com"

    def __init__(self, endpoint, params):
        """
        endpoint: string, ex.: 'v1/forecast'
        params: dict com os query parameters
        """
        self.endpoint = endpoint
        self.params = params

    def get(self):
        url = f"{self.BASE_URL}/{self.endpoint}"
        
        # Para debug, mostra a URL completa:
        query_string = urlencode(self.params)
        full_url = f"{url}?{query_string}"
        print(f"Full URL: {full_url}")

        response = requests.get(url, params=self.params)
        response.raise_for_status()
        return response.json()
