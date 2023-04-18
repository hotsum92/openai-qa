from openai.embeddings_utils import distances_from_embeddings, cosine_similarity

class Answering:
    max_len = 1800

    def __init__(self, openai, repository):
        self.openai = openai
        self.repository = repository

    def create(self, question):
        df=self.repository.load()

        embeddings = self.openai.embedding(question)
        df['distances'] = distances_from_embeddings(embeddings, df['embedding'].values, distance_metric='cosine')

        returns = []
        cur_len = 0

        for i, row in df.sort_values('distances', ascending=True).iterrows():

            cur_len += row['n_token'] + 4
            if cur_len > self.max_len:
                break

            returns.append(row["text"])

        context = "\n\n###\n\n".join(returns)

        response = self.openai.completion(
            f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"情報がありません\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
        )

        return response
