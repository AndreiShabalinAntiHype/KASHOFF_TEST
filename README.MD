# ТЕСТОВОЕ ЗАДАНИЕ KASHOFF

Все зависимости, необходимые для работы программы перечислены в [requirements.txt](requirements.txt) файле.
Для запуска приложения необходимо заполнить .env файл. Пример заполнения можно найти в .env.example.

В качестве базы данных я использовал SQLite.

Команды для запуска:

```{r, engine='bash', count_lines}
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
deactivate
.venv/bin/python main.py
```
