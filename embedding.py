import tiktoken

class Embedding:
    max_tokens = 500

    def __init__(self, openai):
        self.openai = openai
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def start(self, texts):

        modified = [string.replace('。', '.').replace('\n', ' ').replace('\\n', ' ') for string in texts]

        shortened = []

        for text in modified:

            if text is None:
                continue

            n_token = len(self.tokenizer.encode(text))

            if n_token > self.max_tokens:
                shortened += self.split_into_many(text)

            else:
                shortened.append(text)

        for text in shortened:
            n_token = len(self.tokenizer.encode(text))
            embedding = self.openai.embedding(text)

            yield text, n_token, embedding

    def split_into_many(self, text):
        sentences = text.split('.')
        n_tokens = [len(self.tokenizer.encode(" " + sentence)) for sentence in sentences]

        chunks = []
        tokens_so_far = 0
        chunk = []

        for sentence, token in zip(sentences, n_tokens):

            if tokens_so_far + token > self.max_tokens:
                chunks.append(". ".join(chunk) + ".")
                chunk = []
                tokens_so_far = 0

            if token > self.max_tokens:
                continue

            chunk.append(sentence)
            tokens_so_far += token + 1

        if chunk:
            chunks.append(". ".join(chunk) + ".")

        return chunks
