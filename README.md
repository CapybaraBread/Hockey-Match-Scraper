# Hockey Match Scraper

## Описание
Этот проект представляет собой веб-скрапер для сбора информации о хоккейных матчах с сайта **FlashscoreKZ**. 
Скрипт использует **Selenium** для автоматического сбора данных о завершённых матчах, включая команды, счёт, статус и статистику игры.

## Возможности
- Автоматический переход в раздел хоккея.
- Извлечение ID завершённых матчей.
- Получение подробной информации: 
  - Лига
  - Дата и время начала
  - Статус (Завершён, Перерыв и т. д.)
  - Название команд
  - Итоговый счёт
  - Статистические показатели (броски, удаления, процент реализации и др.)
- Форматирование данных в удобочитаемый **DataFrame**.

## Требования
Перед запуском убедитесь, что у вас установлены следующие зависимости:

- Python 3.x
- Selenium
- Pandas
- Google Chrome и ChromeDriver

### Установка зависимостей
Используйте команду для установки всех необходимых пакетов:

```bash
pip3 install selenium pandas
```

Также загрузите и установите **ChromeDriver**, соответствующий вашей версии Google Chrome. Скачать можно [здесь](https://sites.google.com/chromium.org/driver/).

## Установка и запуск
1. Скачайте или склонируйте репозиторий:

```bash
git clone https://github.com/yourusername/hockey-match-scraper.git
cd hockey-match-scraper
```

2. Убедитесь, что **chromedriver** находится в папке проекта или указан правильный путь в коде.

3. Запустите скрипт:

```bash
python3 scraper.py
```

После выполнения программа отобразит таблицу с матчами и их статистикой.

## Вывод данных
Скрипт выводит данные в виде таблицы **pandas DataFrame**, но вы можете сохранить их в CSV:

```python
matches_df.to_csv("matches.csv", index=False)
```

## Возможные ошибки и решения
### 1. `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH`
Решение:
- Проверьте, что **ChromeDriver** установлен и его путь указан в коде.
- Убедитесь, что версия **ChromeDriver** совпадает с версией браузера.

### 2. `ModuleNotFoundError: No module named 'selenium'`
Решение:
- Установите Selenium с помощью `pip3 install selenium`.

### 3. `ElementClickInterceptedException`
Решение:
- Проверьте, не изменился ли сайт и не требует ли он дополнительного взаимодействия (например, закрытия всплывающих окон).

