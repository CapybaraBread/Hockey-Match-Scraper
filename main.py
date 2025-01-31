from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time


custom_options = Options()
custom_options.add_argument("--start-maximized")
path_driver = Service('chromedriver.app')  
driver = webdriver.Chrome(options=custom_options)
link = "https://www.flashscorekz.com"
driver.get(link)

wait = WebDriverWait(driver, 10)


menu_items = driver.find_elements(By.CLASS_NAME, "menuTop__item")
for item in menu_items:
    if item.text.strip().lower() == "хоккей":
        item.click()
        print("Переход в раздел 'Хоккей'")
        break
else:
    print("Кнопка 'Хоккей' не найдена")
    driver.quit()
    exit()


ids = []
matches = driver.find_elements(By.CLASS_NAME, "event__match")
for match in matches:
    if "Завершен" in match.text.splitlines():
        ids.append(match.get_attribute('id')[4:])


matches_data = []

for match_id in ids:
    match_link = f"https://www.flashscorekz.com/match/{match_id}/#/match-summary"
    driver.get(match_link)

    try:
       
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tournamentHeader__country")))

        
        match_data = {}
        match_data["Ссылка"] = match_link
        match_data["Страна турнира"] = driver.find_element(By.CLASS_NAME, "tournamentHeader__country").text
        participants = [el.text for el in driver.find_elements(By.CLASS_NAME, "participant__overflow")]
        match_data["Участники"] = f"{participants[0]} vs {participants[-1]}"
        match_data["Статус"] = driver.find_element(By.CLASS_NAME, "detailScore__status").text
        match_data["Время начала"] = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime").text
        score_wrapper = driver.find_element(By.CLASS_NAME, "detailScore__wrapper").text
        match_data["Счёт"] = f"{score_wrapper[-1]} - {score_wrapper[0]}"

        
        stats_link = f"{match_link}/match-statistics/0"
        driver.get(stats_link)

        try:
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "wcl-row_OFViZ")))
            statistics_elements = driver.find_elements(By.CLASS_NAME, "wcl-row_OFViZ")

            statistics_dict = {}
            for element in statistics_elements:
                static = element.text.splitlines()
                if len(static) >= 3:  
                    value_host = static[0]
                    key = static[1]
                    value_guest = static[2]
                    statistics_dict[key] = f"{value_host} - {value_guest}"
                else:
                    print(f"Пропущен элемент статистики: {static}")

            match_data["Статистика"] = statistics_dict
        except Exception:
            print("Статистика для этого матча отсутствует.")
            match_data["Статистика"] = "-"

        matches_data.append(match_data)

    except Exception as e:
        print(f"Ошибка при обработке матча {match_link}: {e}")


matches_df = pd.DataFrame(matches_data)

def format_statistics(statistics):
    if isinstance(statistics, dict):
        return "\n".join([f"{key}: {value}" for key, value in statistics.items()])
    return statistics

matches_df["Статистика"] = matches_df["Статистика"].apply(format_statistics)


pd.set_option("display.max_columns", None) 
pd.set_option("display.max_colwidth", 100)  
print(matches_df[["Ссылка", "Участники", "Статус", "Счёт", "Статистика"]])

# Закрытие драйвера
driver.quit()
