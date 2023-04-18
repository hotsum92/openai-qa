import unittest
from embedding import Embedding

class Test(unittest.TestCase):

    def test_embedding(self):
        embeddings = {
            "test1": [1, 2, 3],
            "test2": [4, 5, 6],
        }

        openai = MockOpenAIEmbedding(embeddings)
        embedding = Embedding(openai)

        result = embedding.start(["test1", "test2"])

        expected = [
            ("test1", 2,  [1, 2, 3]),
            ("test2", 2, [4, 5, 6]),
        ]

        self.assertEqual(list(result), expected)

class MockOpenAIEmbedding:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def embedding(self, input):
        return self.embeddings[input]
