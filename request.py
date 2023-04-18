import requests

class Request:
    def get(self, url):
        return Response(requests.get(url))

class Response:
    def __init__(self, response):
        self.response = response

    def text(self):
        return self.response.text

