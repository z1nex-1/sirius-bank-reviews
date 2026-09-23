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
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "not-needed"
app = FastAPI()
NUM_REVIEWS = 50
NUM_WORDS = 40
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

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Анализ отзывов</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <h1>Анализ отзывов</h1>
            <h2>Самый положительный отзыв:</h2>
            <p>{most_positive_review}</p>
            <h2>Самый отрицательный отзыв:</h2>
            <p>{most_negative_review}</p>
        </body>
    </html>
    """.format(
        most_positive_review=df.loc[df['sentiment'].idxmax(), 'review'],
        most_negative_review=df.loc[df['sentiment'].idxmin(), 'review']
    )

def analyze_sentiment(review):
    messages = [
        {"role": "system", "content": "Вы помощник по анализу тональности. Оцените тональность на отзыв о банке  от 1 до 100 , где ниже 20 - плохо, а выше 80 - хорошо.Когда сомневаешься - занижай. Отвечай только цифры"},
        {"role": "user", "content": f"Оцените тональность следующего отзыва: {review}"}
    ]

    try:
        start_time = time.time()
        completion = openai.ChatCompletion.create(
            model="local-model",
            messages=messages,
            temperature=0.7,
        )
        end_time = time.time()

        response = completion.choices[0].message.content.strip()
        score_match = re.search(r'(\d+)', response)

        if score_match:
            score = int(score_match.group(1))
            if 1 <= score <= 100:
                print(f"Отзыв: {review} : {score} : {end_time - start_time} сек.\n")
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
    if top_positive_words:
        wordcloud_pos = WordCloud(width=WORD_CLOUD_WIDTH, height=WORD_CLOUD_HEIGHT, background_color='white', colormap=cmap_positive, max_words=NUM_WORDS).generate_from_frequencies(top_positive_words)
        ax[1, 0].imshow(wordcloud_pos)
        ax[1, 0].set_title("Облако слов для положительных отзывов")
        ax[1, 0].axis("off")
    else:
        ax[1, 0].text(0.5, 0.5, "Нет данных для облака слов", transform=ax[1, 0].transAxes, va='center', ha='center', fontsize=FONTSIZE, color='black')
        ax[1, 0].axis("off")

    ax[0, 1].text(0.05, 0.5, f"Худший отзыв:\n\n{most_negative['username']}\n{most_negative['review']}", transform=ax[0, 1].transAxes, va='center', fontsize=FONTSIZE, color='darkred')
    ax[0, 1].axis("off")

    top_negative_words = get_top_words(negative_reviews)
    if top_negative_words:
        wordcloud_neg = WordCloud(width=WORD_CLOUD_WIDTH, height=WORD_CLOUD_HEIGHT, background_color='white', colormap=cmap_negative, max_words=NUM_WORDS).generate_from_frequencies(top_negative_words)
        ax[1, 1].imshow(wordcloud_neg)
        ax[1, 1].set_title("Облако слов для отрицательных отзывов")
        ax[1, 1].axis("off")
    else:
        ax[1, 1].text(0.5, 0.5, "Нет данных для облака слов", transform=ax[1, 1].transAxes, va='center', ha='center', fontsize=FONTSIZE, color='black')
        ax[1, 1].axis("off")

    plt.tight_layout(pad=0, w_pad=2)
    plt.show()

positive_file_path = 'positive_reviews.txt'
with open(positive_file_path, 'w', encoding='utf-8') as positive_file:
    positive_file.write('\n\n'.join(df[df['sentiment'] >= 80]['review'].tolist()))
print(f"\nПоложительные отзывы записаны в файл: {positive_file_path}")

negative_file_path = 'negative_reviews.txt'
with open(negative_file_path, 'w', encoding='utf-8') as negative_file:
    negative_file.write('\n\n'.join(df[df['sentiment'] < 80]['review'].tolist()))
print(f"Отрицательные отзывы записаны в файл: {negative_file_path}")

generate_word_clouds(df[df['sentiment'] >= 80]['review'].tolist(), df[df['sentiment'] < 80]['review'].tolist(), most_positive, most_negative)
