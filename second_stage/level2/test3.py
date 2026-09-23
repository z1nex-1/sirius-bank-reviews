import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import hdbscan
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import string
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text.lower())
    stop_words = stopwords.words('russian')
    tokens = [word for word in tokens if word not in stop_words]
    stemmer = SnowballStemmer('russian')
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

def main():
    file_path = 'sravni.json'
    df = load_data(file_path)
    df['processed_review'] = df['review_text'].apply(preprocess_text)

    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['processed_review'])

    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=1, gen_min_span_tree=True)
    df['hdbscan_cluster'] = clusterer.fit_predict(tfidf_matrix.toarray())

    pd.set_option('display.max_colwidth', None)
    for cluster in set(df['hdbscan_cluster']):
        print(f"Кластер {cluster}:\n")
        print(df[df['hdbscan_cluster'] == cluster]['review_text'].head().to_string(index=False), "\n")

if __name__ == "__main__":
    main()
