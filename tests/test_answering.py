import unittest
import pandas
from answering import Answering

class Test(unittest.TestCase):
    def test_answering(self):
        embeddings = {
            "test": [1, 2, 3],
        }

        df = pandas.DataFrame(
            {
                "text": ["test1", "test2"],
                "n_token": [2, 2],
                "embedding": [[1, 2, 3], [4, 5, 6]],
            }
        )

        openai = MockOpenAICompletion(embeddings, "answer")
        repository = MockRepository(df)

        answering = Answering(openai, repository)

        result = answering.create("test")

        expected = "answer"

        self.assertEqual(result, expected)

class MockOpenAICompletion:
    def __init__(self, embeddings, response):
        self.embeddings = embeddings
        self.response = response

    def embedding(self, input):
        return self.embeddings[input]

    def completion(self, prompt):
        return self.response

class MockRepository:
    def __init__(self, df):
        self.df = df

    def load(self):
        return self.df

