import json
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.cluster import AgglomerativeClustering
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt', quiet=True)

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def prepare_for_doc2vec(df):
    documents = [TaggedDocument(words=word_tokenize(doc.lower()), tags=[i]) for i, doc in enumerate(df['review_text'])]
    return documents

def train_doc2vec(documents):
    model = Doc2Vec(documents, vector_size=100, window=2, min_count=1, workers=4, epochs=40)
    return model

def get_doc_vectors(model, documents):
    vectors = [model.infer_vector(doc.words) for doc in documents]
    return vectors

def main():
    file_path = 'sravni.json'
    df = load_data(file_path)
    documents = prepare_for_doc2vec(df)
    model = train_doc2vec(documents)
    doc_vectors = get_doc_vectors(model, documents)

    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.5)
    df['cluster'] = clustering.fit_predict(doc_vectors)

    for i in set(df['cluster']):
        print(f"Кластер {i}:\n", df[df['cluster'] == i]['review_text'].head(), "\n")

if __name__ == "__main__":
    main()
