import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
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

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['processed_review'])

    kmeans = KMeans(n_clusters=5)
    df['cluster'] = kmeans.fit_predict(tfidf_matrix)

    for i in range(5):
        print(f"Кластер {i}:\n", df[df['cluster'] == i]['review_text'].head(), "\n")

if __name__ == "__main__":
    main()
