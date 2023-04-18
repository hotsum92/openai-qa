import unittest
from crawler import Crawler

class Test(unittest.TestCase):
    def test_crawl(self):
        pages = {
            "https://example.com": "<html><body><a href='https://example.com/1'>from parent</a></body></html>",
            "https://example.com/1": "<html><body><a href='https://example.com/1'>child</a></body></html>",
        }

        request = MockRequest(pages)

        crawler = Crawler(request)
        result = list(crawler.start("https://example.com"))

        expected = [
            ("https://example.com", "from parent"),
            ("https://example.com/1", "child"),
        ]

        self.assertEqual(result, expected)

class MockResponse:
    def __init__(self, text):
        self.row_text = text

    def text(self):
        return self.row_text

class MockRequest:
    def __init__(self, pages):
        self.pages = pages

    def get(self, url):
        if url in self.pages:
            return MockResponse(self.pages[url])
        else:
            raise ValueError("Unknown URL: " + url)

