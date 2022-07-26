import os
import warnings

import fasttext.util
import nltk
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

from preprocessing.preprocessing import Preprocessor

warnings.filterwarnings('ignore')

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')


class DataReader:
    def __init__(self, read_from_excels=False):
        if read_from_excels:
            preprocessor = Preprocessor()
            dfs = []
            for file in tqdm(os.listdir("./Excels")):
                df = pd.read_excel(os.path.join("./Excels", file))
                dfs.append(df)
            df = pd.concat(dfs)

            df = df[df['Language'] == 'en']
            df.reset_index(drop=True, inplace=True)
            df.drop_duplicates(subset="Text", keep='first', inplace=True, ignore_index=True)
            df = preprocessor.perform_clean_lemmatize_tokenize(df)
            idx = df.Text_words.apply(len) > df.Text_words.apply(len).describe()["25%"]
            df = df[idx]

            df["Text_words_joined"] = df.Text_words.apply(lambda x: " ".join(x))
            df.drop_duplicates(subset="Text_words_joined", keep='first', inplace=True, ignore_index=True)
            self.df = df

        else:
            df = pd.read_csv("./data_final.csv")
            df["Text_words"] = df.Text_words_joined.apply(lambda x: x.split(" "))
            df.drop("Unnamed: 0", axis=1, inplace=True)
            self.df = df


data_reader = DataReader(read_from_excels=False)
df = data_reader.df


class TFIDFSearch:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.vocabulary = list(set(df['Text_words'].explode()) - {np.nan})

        self.tfidf = TfidfVectorizer(vocabulary=self.vocabulary)
        self.tfidf_tran = self.tfidf.fit_transform(df['Text_words'].apply(lambda x: ' '.join(x)))

    def get_vector(self, tokens):
        result = np.zeros((len(self.vocabulary)))
        x = self.tfidf.transform(tokens)
        for token in tokens:
            try:
                ind = self.vocabulary.index(token)
                result[ind] = x[0, self.tfidf.vocabulary_[token]]
            except Exception as e:
                print(e)
                pass
        return result

    @staticmethod
    def cosine_sim(a, b):
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0
        cos_sim = np.dot(a, b) / (norm_a * norm_b)
        return cos_sim

    def search(self, k, query):
        tokens = self.preprocessor.clean_query(query)
        tokens = [token for token in tokens if token in self.vocabulary]
        print(tokens)
        q_df = pd.DataFrame(columns=['q_clean'])
        q_df.loc[0, 'q_clean'] = tokens

        d_cosines = []

        query_vector = self.get_vector(tokens)
        print(sum(query_vector))
        for d in self.tfidf_tran.A:
            d_cosines.append(self.cosine_sim(query_vector, d))

        out = np.array(d_cosines).argsort()[-k:][::-1]
        a = pd.DataFrame()
        for i, index in enumerate(out):
            a.loc[i, 'index'] = str(index)
            a.loc[i, 'text'] = df.iloc[index]['Text']
            a.loc[i, 'words'] = str(df.iloc[index]['Text_words'])
            a.loc[i, 'Score'] = d_cosines[int(index)]
        return a


class BooleanSearch:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.vocabulary = list(set(df['Text_words'].explode()) - {np.nan})
        self.vocabulary_index = {word: idx for idx, word in enumerate(self.vocabulary)}
        self.mat = np.zeros((len(df), len(self.vocabulary)), )
        for index, row in df.iterrows():
            for token in row['Text_words']:
                self.mat[index][self.vocabulary_index[token]] = 1

    def search(self, k, query):
        tokens = self.preprocessor.clean_query(query)
        query_vector = []
        for token in tokens:
            if token in self.vocabulary_index:
                query_vector.append(self.vocabulary_index[token])
        out = []
        for index, vec in enumerate(self.mat):
            flag = True
            for token_index in query_vector:
                if vec[token_index] == 0:
                    flag = False
                    break
            if flag:
                out.append(index)
            if len(out) == k:
                break
        print(out)
        a = pd.DataFrame()
        for i, index in enumerate(out):
            a.loc[i, 'index'] = str(index)
            a.loc[i, 'text'] = df.iloc[index]['Text']
            a.loc[i, 'words'] = str(df.iloc[index]['Text_words'])

        return a


class FastText:
    def __init__(self):
        self.preprocessor = Preprocessor()
        fasttext.util.download_model('en', if_exists='ignore')  # English
        self.ft = fasttext.load_model("./cc.en.300.bin")

        self.text_vectors = []
        self.words_count = []
        for _, row in df.iterrows():
            self.words_count.append(len(row['Text_words']))
            self.text_vectors.append(self.tokens_to_vec(row['Text_words']))

    def tokens_to_vec(self, tokens):
        cur_vectors = []
        if len(tokens) == 0:
            return np.zeros(self.ft.get_dimension())
        for token in tokens:
            cur_vectors.append(self.ft.get_word_vector(token))
        return np.asarray(np.average(cur_vectors, axis=0, keepdims=True))[0]

    @staticmethod
    def cosine_sim(a, b):
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0
        cos_sim = np.dot(a, b) / (norm_a * norm_b)
        return cos_sim

    def search(self, k, query):
        tokens = self.preprocessor.clean_query(query)
        query_vector = self.tokens_to_vec(tokens)
        d_cosines = []
        print(tokens)
        for idx, d in enumerate(self.text_vectors):
            d_cosines.append(self.cosine_sim(d, query_vector))
            if self.words_count[idx] > 10:
                d_cosines[-1] += 0.2
            elif self.words_count[idx] > 5:
                d_cosines[-1] += 0.1

        out = np.array(d_cosines).argsort()[-k:][::-1]
        a = pd.DataFrame()
        for i, index in enumerate(out):
            a.loc[i, 'index'] = str(index)
            a.loc[i, 'text'] = df.iloc[index]['Text']
            a.loc[i, 'words'] = str(df.iloc[index]['Text_words'])
            a.loc[i, 'Score'] = d_cosines[int(index)]
        return a


class TransformerSearch:
    def __init__(self):
        self.model = SentenceTransformer('../transformer-model')
        self.preprocessor = Preprocessor()
        self.all_embeddings = np.load("./transformer_embeddings.npy")

    def search(self, k, query):
        cleaned = self.preprocessor.clean_query(query)
        cleaned = ' '.join(cleaned)
        encoded_q = self.model.encode([cleaned])
        scores = np.array([(1 - cosine(doc, encoded_q)) for doc in self.all_embeddings])
        tops = scores.argsort()[-k:][::-1]
        print(tops)

        a = pd.DataFrame()
        for i, index in enumerate(tops):
            a.loc[i, 'index'] = str(index)
            a.loc[i, 'text'] = df.iloc[index]['Text']
            a.loc[i, 'words'] = str(df.iloc[index]['Text_words'])
            a.loc[i, 'Score'] = scores[int(index)]
        return a


models = [FastText(), BooleanSearch(), TFIDFSearch(), TransformerSearch()]
