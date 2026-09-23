import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

additional_stop_words = ['банк', 'банка', 'тинькофф', 'тинькоффа', 'тинькоф', 'тинькофа']

def load_and_preprocess_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    
    stop_words = stopwords.words('russian') + additional_stop_words
    stemmer = SnowballStemmer('russian')
    
    def preprocess_text(text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    
    df['processed_review'] = df['review_text'].apply(preprocess_text)
    return df

def analyze_reviews(file_path):
    df = load_and_preprocess_data(file_path)
    num_reviews = len(df)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['processed_review'])
    kmeans = KMeans(n_clusters=10)
    df['cluster'] = kmeans.fit_predict(X)
    
    for i in range(10):
        cluster_text = " ".join(df[df['cluster'] == i]['processed_review'].values)
        generate_word_cloud(cluster_text, i)
    
    for i in range(10):
        try:
            cluster_center_idx = cosine_similarity(np.asarray(X[df['cluster'] == i].toarray()), np.asarray(X[df['cluster'] == i].mean(axis=0).reshape(1, -1))).argmax()
            cluster_center_review = df[df['cluster'] == i].iloc[cluster_center_idx]['review_text']
            similar_reviews_indices = cosine_similarity(np.asarray(X[df['cluster'] == i].toarray()), np.asarray(X[df['cluster'] == i].mean(axis=0).reshape(1, -1))).argsort(axis=0)[-6:][::-1].flatten()
            similar_reviews = df[df['cluster'] == i].iloc[similar_reviews_indices][1:]['review_text'].values
            create_html_page(i, cluster_center_review, similar_reviews, num_reviews)
        except Exception as e:
            print(f"An error occurred while processing cluster {i}: {e}")

def generate_word_cloud(text, cluster_num):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f"cluster_{cluster_num}_wordcloud.png")
    plt.close()

def create_html_page(cluster_num, cluster_center_review, similar_reviews, num_reviews):
    with open("cluster_analysis.html", "a", encoding="utf-8") as f:
        if cluster_num == 0:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n")
            f.write("<meta charset='UTF-8'>\n")
            f.write("<title>Анализ отзывов банка Тинькофф</title>\n")
            f.write(f"<h2>Количество проанализированных отзывов: {num_reviews}</h2>\n")
            f.write("<h2>Методы обработки данных:</h2>\n")
            f.write("<p>1. Предобработка текста (приведение к нижнему регистру, удаление пунктуации, токенизация, стемминг)</p>\n")
            f.write("<p>2. Векторизация текста с использованием TF-IDF (Term Frequency-Inverse Document Frequency)</p>\n")
            f.write("<p>3. Кластеризация методом KMeans</p>\n")
            f.write("</head>\n<body>\n")

        f.write(f"<h1>Анализ кластера {cluster_num}</h1>\n")
        f.write("<h2>Средний отзыв кластера:</h2>\n")
        f.write(f"<p>{cluster_center_review}</p>\n")
        
        f.write(f"<img src='cluster_{cluster_num}_wordcloud.png' alt='Облако слов кластера {cluster_num}'>\n")
        f.write("<h2>Схожие отзывы:</h2>\n")
        
        for review in similar_reviews:
            f.write(f"<p>{review}</p>\n")
        
        if cluster_num == 9:
            f.write("</body>\n</html>")

if __name__ == "__main__":
    with open("cluster_analysis.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<title>Анализ отзывов банка Тинькофф</title>\n")
        f.write("</head>\n<body>\n")

    analyze_reviews('sravni.json')
