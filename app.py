from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import os
import pandas
from crawler import Crawler
from request import Request, Response
from openaiapi import OpenAiApi
from embedding import Embedding
from answering import Answering
from repository import Repository

api_key = os.environ["OPENAI_API_KEY"]

class HTTPHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'OK')
            return

        if parsed_path.path.startswith('/static'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            with open(parsed_path.path[1:], 'r') as f:
                content = f.read()

            self.wfile.write(content.encode())
            return

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Not Found')
        return

    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/crawl':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            json_data = json.loads(body)
            url = json_data['url']


            if not os.path.exists('tmp'):
                os.makedirs('tmp')

            crawler = Crawler(Request())
            crawler_result = list(crawler.start(url))

            embedding = Embedding(OpenAiApi(api_key))
            embedding_result = embedding.start(map(lambda x: x[1], crawler_result))

            repository = Repository()
            repository.save(embedding_result)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'OK')

            return

        if parsed_path.path == '/question':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            json_data = json.loads(body)
            question = json_data['question']

            answering = Answering(OpenAiApi(api_key), Repository())

            answer = answering.create(question)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(answer.encode())

            return

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Not Found')
        return

address = ('0.0.0.0', 8080)

print('app is running on port 8080...')
print('press ctrl+c to stop')

with HTTPServer(address, HTTPHandler) as server:
    server.serve_forever()
