## Ридми будет доделан 17.12.2025 к вечеру
```
git clone https://github.com/artem-sitd/video_bot.git
cd video_bot

Создаем вирт. окружение
python -m venv venv

Активируем его
source venv/bin/activate

Устанавливаем зависимости
pip install -r requirements.txt

Копируем .env
cp .env.example .env
И заполняем его

Создать БД, пользователя, сделать владельцем
CREATE DATABASE videos_db;
CREATE USER videos_user WITH PASSWORD '123';
ALTER DATABASE videos_db OWNER TO videos_user;

Применить миграции
alembic revision --autogenerate -m "init tables"
alembic upgrade head

Запустить скрипт на заполнение тестовыми данными videos.json
python app/loader/load_json.py

Запустить бота
python bot/main.py```


Вебхуки не используем, будет работать через полинг.
```



