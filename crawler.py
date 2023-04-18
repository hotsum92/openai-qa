from collections import deque
from bs4 import BeautifulSoup

class Crawler:

    limit_pages = 3

    def __init__(self, request):
        self.request = request

    def start(self, url):
        queue = deque([url])
        seen = set([url])

        while queue:
            if len(seen) > self.limit_pages:
                break

            link = queue.pop()
            response = self.request.get(link)

            soup = BeautifulSoup(response.text(), "html.parser")
            text = soup.get_text()

            yield link, text

            for tag in soup.find_all('a'):
                href = tag.get('href')
                if href not in seen:
                    queue.append(href)
                    seen.add(href)
