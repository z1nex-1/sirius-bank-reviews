# Анализ клиентских отзывов о банке

Проект команды на отборе «Сириус ИИ», весна 2024. Задача — по отзывам клиентов Тинькофф
понять, чем люди довольны и на что жалуются: собрать отзывы, оценить тональность и выделить
основные темы.

<p>
  <img src="second_stage/level2/cluster_3_wordcloud.png" width="49%" alt="Облако слов одного из кластеров">
  <img src="img/im4.png" width="49%" alt="Локальная модель в LM Studio">
</p>

**Презентация:** [presentationforsirius.pdf](presentationforsirius.pdf)

## Этап 1. Тональность с помощью локальной LLM

Модель **zephyr-7b-beta (Q4_K_S)** запускали в LM Studio как локальный сервер с
OpenAI-совместимым API. Скрипт отправляет каждый отзыв с просьбой оценить тональность от 1 до
100, делит отзывы на положительные и отрицательные и строит облака слов для обеих групп вместе
с самым лучшим и самым худшим отзывом.

<p>
  <img src="img/img5.png" width="49%" alt="Запрос к модели">
  <img src="img/img7.png" width="49%" alt="Проблемы клиентов, сформулированные моделью">
</p>

- `fo_sir_tink/localSemantic.py` — оценка тональности и облака слов
- `fo_sir_tink/table_excel_load.py` — модель формулирует проблему клиента одной фразой, результат складывается в Excel
- `fo_sir_tink/wordcloud_base.py` — облака слов без модели, по готовым оценкам

## Этап 2. Сбор отзывов и поиск тем

Собрали отзывы с двух сайтов разными способами:

| | banki.ru | sravni.ru |
|---|---|---|
| Инструменты | requests + BeautifulSoup | Selenium + webdriver-manager |
| Как | обычные GET-запросы по страницам отзывов | браузер листает ленту и раскрывает каждый отзыв кнопкой «Читать» |
| Очистка | удаление HTML и служебных символов | не нужна |

Дальше тексты привели к одному виду (стоп-слова, стемминг, пунктуация), перевели в TF-IDF
и разбили KMeans на 10 кластеров. Для каждого кластера программа строит облако слов и
находит пять самых типичных отзывов, а итог собирает в HTML-отчёт
[`cluster_analysis.html`](second_stage/level2/cluster_analysis.html). Оценку тональности на
этом этапе не делали: для русского языка нужна модель уровня BERT, и мы честно оставили это
на следующий шаг.

<p>
  <img src="img/img8.png" width="49%" alt="Парсер banki.ru">
  <img src="img/img13.png" width="49%" alt="TF-IDF и кластеризация">
</p>

- `second_stage/theme5.ipynb` — парсер banki.ru и предобработка
- `second_stage/level2/sravnyParser.py` — парсер sravni.ru, результат в `sravni.json`
- `second_stage/level2/Main.py` — кластеризация, облака слов и HTML-отчёт
- `second_stage/level2/test*.py` — эксперименты: Doc2Vec, HDBSCAN, n-граммы, VADER

## Запуск

```bash
pip install -r second_stage/level2/requirements.txt
cd second_stage/level2
python Main.py
```

Первый этап требует запущенного LM Studio с моделью на `localhost:1234`:

```bash
pip install -r fo_sir_tink/requirements.txt
cd fo_sir_tink
python localSemantic.py
```

## Команда

- Павел Кончаков
- Илья Григорьев — [z1nex-1](https://github.com/z1nex-1)
- Владимир Аксенов
- Дмитрий Дырков
