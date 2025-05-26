# **Сириус ИИ** Весна 2024

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/logo1.png" width="300" />
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/logo2.png" width="150" />
</p>

## Инструмент для анализа клиентских отзывов

### Проектная команда:

- Кончаков Павел
- Григорьев Илья
- Аксенов Владимир
- Дырков Дмитрий

________

# 1 Этап

Для первого этапа мы решили использовать модель **zephyr beta 7B Q4_K_S**

Мы запускаем ее в **LM Studio**, а потом уже в программе на языке программирования **python** обращаемся к серверу.

## Демонстрация работы

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/im4.png" width="500" />
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img5.png" width="500" />
</p>

## Результат

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img6.png" width="500" />
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img7.png" width="500" />
</p>

## Видеодемострация работы для первого этапа

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/qr.png" width="300" />
</p>

________________________________

# 2 Этап
### Вот второй этап опишем подробно
## План реализации 
1. Сбор информации
2. Чистим от лишнего и структурируем собранные данные для последующего анализа
3. Извлечение признаков

## Сбор информации
### Для сбора информации мы использовали 2 вида парсерова с 2 источников

Colons can be used to align columns.

|   Сайт           | banki.ru            | sravni.ru                            |
| -------------    |:-------------:      | :-----:                               |
| Что использовали?| **bs4** и **urlib** | **selenium** и **webdriver_manager** |
| Как работает?    | Просто через **get** запросы     | Ходим по сайт через **ChromeDriver** и нажимем на кнопки |

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img8.png" width="450" />
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img9.png" width="550" />
</p>

## Обработка информации 
+ Парсер banki.ru потребовал дополнительную чистку от 
HTML-cимволов для чистки.
+ Парсер sravni.ru устроен так, что после парсинга не требуется дополнительная чистка.

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img10.png" width="500" />
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img11.png" width="500" />
</p>

## Извлечение признаков
+ Провели предварительную обработку текстов: удаление стоп-слов, лемматизацию / стемминг, удаление пунктуации. 

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img12.png" width="1000" />
</p>

+ Преобразовали собранные тексты отзывов в векторное представление с использованием методов NLP, таких как TF-IDF. 

<p float="left">
  <img src="https://github.com/z1nex-1/Sirius_AI/blob/main/img/img13.png" width="1000" />
</p>

## Анализ и интерпретация отзывов
+ Использовали полученные признаки для выявления общих тем и тенденций в собранных отзывах. Сделали векторизацию на 10 кластеров. Анализа настроений нет - там надо применять что-то посерьезней ,хотя бы модель типа bert, появляются сложности с русским языком. 
Такой анализ в HTML-формате генерирует наша программа(только не 4, а 10 кластеров).

### Подробнее о всех этапах нашей работы вы можете узнать в файл **presentationforsirius.pdf**

______

# Вывод
### Ждем встречи 1 апреля в 13:00!

_____
# Содержание репозитория
+ fo_sir_tink - все файлы первого этапа, в которые входят:
  + req.txt - requierments
  + localSemantic.py - анализ семантики и распределения всех отзывов на положительные и отрицательные
  + table_excel_load.py - загрузка отзывов в таблицу excel
  + wordcloud_base.py - создание облаков слов
+ second_stage - все файлы второго этапа, а именно:
  + level2 - папка, содержащая парсер с сайта **sravni.ru** а также 4 тестовых питон файла
  + theme5.ipynb - блокнот jupiter notebook с парсером для **banki.ru** а также стемминг и лемматизация
  + LICENSE.chromedriver - лицензия для запуска парсера **sravni.ru**
+ img - папка с фотографиями для файла README.md
+ presentationforsirius.pdf - наша презентация
