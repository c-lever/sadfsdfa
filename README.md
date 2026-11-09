```bash
# скачивание зависимостей
pip install -r requirements.txt

# настройка окружения: замените плейсхолдеры на реальные значения
cp .env.example .env

# запуск дб
postgres \
    -D "ДИРЕКТОРИЯ ДБ" \
    -k "ДИРЕКТОРИЯ СОКЕТА ДБ" \
    -h "IP из .env" \
    -p "PORT из .env"

# запуск апи
uvicorn app.main:app --reload
```
