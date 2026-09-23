import openai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from wordcloud import WordCloud, STOPWORDS
from matplotlib.colors import LinearSegmentedColormap
from collections import Counter
import os

openai.api_base = "http://localhost:1234/v1"
openai.api_key = "not-needed"

NUM_REVIEWS = 10
NUM_WORDS = 20
WORD_CLOUD_WIDTH = 1000
WORD_CLOUD_HEIGHT = 700
FIGSIZE = (16, 12)
HEIGHT_RATIOS = [1, 6]
FONTSIZE = 12
hspace = 0.05


print("Ключ API OpenAI загружен успешно")

df = pd.read_csv("samples.csv", delimiter=';', names=['id', 'username', 'review'], encoding='utf-8').head(NUM_REVIEWS)
print("CSV файл загружен успешно")
print(f"Количество отзывов: {len(df)}")

def analyze_sentiment(review):
    messages = [
        {"role": "system", "content": "Вы помощник по анализу тональности. Оцените тональность следующего отзыва в диапазоне от 1 до 100."},
        {"role": "user", "content": f"Оцените тональность следующего отзыва: {review}"}
    ]

    try:
        completion = openai.ChatCompletion.create(
            model="local-model",
            messages=messages,
            temperature=0,
        )

        response = completion.choices[0].message.content.strip()
        score_match = re.search(r'(\d+)', response)

        if score_match:
            score = int(score_match.group(1))
            if 1 <= score <= 100:
                return score
            else:
                return np.nan
        else:
            return np.nan
    except Exception as e:
        print(f"Ошибка: {e}")
        return np.nan

df['sentiment'] = df['review'].apply(analyze_sentiment)
print("Анализ тональности завершен")

most_positive = df.loc[df['sentiment'].idxmax()]
most_negative = df.loc[df['sentiment'].idxmin()]
print("\nСамый положительный отзыв:")
print(most_positive[['id', 'username', 'review', 'sentiment']])
print("\nСамый отрицательный отзыв:")
print(most_negative[['id', 'username', 'review', 'sentiment']])

colors_positive = [(0.0, 'lightgreen'), (1.0, 'darkgreen')]
cmap_positive = LinearSegmentedColormap.from_list('positive_cmap', colors_positive)

colors_negative = [(0.0, 'lightcoral'), (1.0, 'darkred')]
cmap_negative = LinearSegmentedColormap.from_list('negative_cmap', colors_negative)

def get_top_words(reviews, excluded_words_file='excluded_words.txt', num_words=NUM_WORDS):
    all_words = re.findall(r'\w+', ' '.join(reviews).lower())
    counter = Counter(all_words)

    if os.path.exists(excluded_words_file):
        with open(excluded_words_file, 'r', encoding='utf-8') as f:
            excluded_words = f.read().strip().split(',')
    else:
        excluded_words = []

    stopwords_and_excluded = set(STOPWORDS).union(set(excluded_words))

    top_words = [word for word in counter.most_common(num_words) if word[0] not in stopwords_and_excluded]
    return dict(top_words)

def generate_word_clouds(positive_reviews, negative_reviews, most_positive, most_negative):
    fig, ax = plt.subplots(2, 2, figsize=FIGSIZE, facecolor='none', gridspec_kw={'height_ratios': HEIGHT_RATIOS, 'hspace': hspace})

    ax[0, 0].text(0.05, 0.5, f"Лучший отзыв:\n\n{most_positive['username']}\n{most_positive['review']}", transform=ax[0, 0].transAxes, va='center', fontsize=FONTSIZE, color='darkgreen')
    ax[0, 0].axis("off")

    top_positive_words = get_top_words(positive_reviews)
    wordcloud_pos = WordCloud(width=WORD_CLOUD_WIDTH, height=WORD_CLOUD_HEIGHT, background_color='white', colormap=cmap_positive, max_words=NUM_WORDS).generate_from_frequencies(top_positive_words)
    ax[1, 0].imshow(wordcloud_pos)
    ax[1, 0].set_title("Облако слов для положительных отзывов")
    ax[1, 0].axis("off")

    ax[0, 1].text(0.05, 0.5, f"Худший отзыв:\n\n{most_negative['username']}\n{most_negative['review']}", transform=ax[0, 1].transAxes, va='center', fontsize=FONTSIZE, color='darkred')
    ax[0, 1].axis("off")

    top_negative_words = get_top_words(negative_reviews)
    wordcloud_neg = WordCloud(width=WORD_CLOUD_WIDTH, height=WORD_CLOUD_HEIGHT, background_color='white', colormap=cmap_negative, max_words=NUM_WORDS).generate_from_frequencies(top_negative_words)
    ax[1, 1].imshow(wordcloud_neg)
    ax[1, 1].set_title("Облако слов для отрицательных отзывов")
    ax[1, 1].axis("off")

    plt.tight_layout(pad=0, w_pad=2)
    plt.show()

positive_reviews = df[df['sentiment'] >= 80]['review'].tolist()
negative_reviews = df[df['sentiment'] <= 20]['review'].tolist()

generate_word_clouds(positive_reviews, negative_reviews, most_positive, most_negative)
