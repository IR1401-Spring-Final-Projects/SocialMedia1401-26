import nltk
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from preprocessing.preprocessing import Preprocessor

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

df = pd.read_csv("data_final.csv")
df["Text_words"] = df.Text_words_joined.apply(lambda x: x.split(" "))
df.drop("Unnamed: 0", axis=1, inplace=True)
emb = np.load("transformer_embeddings.npy")
kmeans = KMeans(init="k-means++", n_clusters=10)
kmeans.fit(emb)
y = kmeans.labels_

pca = PCA(n_components=2).fit_transform(emb)

preprocessor = Preprocessor()
model = SentenceTransformer('all-MiniLM-L6-v2')


def find_cluster(query):
    query_embeddings = model.encode(" ".join(preprocessor.clean_query(query)))

    qy = kmeans.predict(np.array([query_embeddings], dtype=np.float32))
    label = qy[0]
    print("-" * 100)
    print(f"Query: {query}")
    print(f"Cluster: {label}")
    print(f"Key-words of this cluster:")
    print(" ".join(df[y == label].Text_words.explode().value_counts().head(15).index.to_list()))
    return {
        "cluster": str(label),
        "keywords": df[y == label].Text_words.explode().value_counts().head(15).index.to_list()
    }
