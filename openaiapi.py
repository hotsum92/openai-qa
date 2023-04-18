import openai

class OpenAiApi:

    max_tokens = 150
    stop_sequence = None


    def __init__(self, api_key):
        openai.api_key = api_key

    def embedding(self, text):
        return openai.Embedding.create(input=text,
                                       model='text-embedding-ada-002')['data'][0]['embedding']

    def completion(self, prompt):
        return openai.Completion.create(
            prompt=prompt,
            temperature=0,
            max_tokens=self.max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=self.stop_sequence,
            model="text-davinci-003",
        )["choices"][0]["text"].strip()

