import pandas
import numpy

class Repository:

    path = 'tmp/embedding.csv'

    def save(self, embedding):
        df = pandas.DataFrame(embedding, columns=['text', 'n_token', 'embedding'])
        df.to_csv(self.path)

    def load(self):
        df= pandas.read_csv(self.path, index_col=0)
        df['embedding'] = df['embedding'].apply(eval).apply(numpy.array)
        return df
