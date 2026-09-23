from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

NUM_REVIEWS_TO_LOAD = 100

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

driver.get("https://www.sravni.ru/bank/tinkoff-bank/otzyvy/")

review_data = []

try:
    loaded_reviews = 0
    while loaded_reviews < NUM_REVIEWS_TO_LOAD:
        reviews = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".review-card_wrapper__gnPSK")))
        
        last_review = reviews[-1]
        driver.execute_script("arguments[0].scrollIntoView(true);", last_review)
        time.sleep(1)

        for review in reviews[loaded_reviews:]:
            try:
                read_more_button = review.find_element(By.CSS_SELECTOR, "a.h-ml-4._p7lcln._7k5cz5")
                driver.execute_script("arguments[0].scrollIntoView(true);", read_more_button)
                time.sleep(1)
                read_more_button.click()
                time.sleep(1)
            except Exception as e:
                print("Кнопка 'Читать' не найдена или другая ошибка:", e)

            try:
                name = review.find_element(By.CSS_SELECTOR, ".h-color-D100._1h41p0x._1livb46._1gpt55s").text
                date = review.find_element(By.CSS_SELECTOR, ".h-color-D30._1h41p0x").text
                rating_elements = review.find_elements(By.CSS_SELECTOR, "._e7kry4._akgnn3 span[data-qa='Icon']")
                rating = len(rating_elements)
                review_text_element = review.find_element(By.CSS_SELECTOR, ".review-card_text__jTUSq")
                review_text = review_text_element.text.replace("\nЧитать", "").rstrip()

                if review_text.endswith("Скрыть"):
                    review_text = review_text[:-6]

                review_info = {
                    "name": name,
                    "date": date,
                    "rating": rating,
                    "review_text": review_text
                }

                print(review_info)
                review_data.append(review_info)
                loaded_reviews += 1

                if loaded_reviews >= NUM_REVIEWS_TO_LOAD:
                    break
            except Exception as e:
                print("Ошибка при извлечении данных отзыва:", e)

finally:
    with open("sravni.json", "w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=4)

    driver.quit()
