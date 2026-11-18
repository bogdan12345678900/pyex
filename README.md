# SeaCrew — сайт крюинговой компании (Django)

Поиск вакансий для моряков, анкета моряка, запрос экипажа для судовладельцев, админка для менеджеров.

## Запуск

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations crew
python manage.py migrate
python manage.py seed_demo      # ~35 демо-вакансий (--force — пересоздать)
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/ · Админка: http://127.0.0.1:8000/admin/

## Структура
- `crew/models.py` — типы судов, должности, вакансии, анкеты моряков, запросы судовладельцев
- `crew/views.py` — главная, список и карточка вакансии, анкета, форма для судовладельцев
- `crew/templates/crew/` — шаблоны, `static/css/site.css` — морская тема
- Анкеты и запросы смотрите в админке (отметка «Обработана»)

Перед публикацией: задайте свой `SECRET_KEY`, `DEBUG = False` и `ALLOWED_HOSTS` в `config/settings.py`.

## Картинки
- Иллюстрации судов (`static/img/*.svg`) нарисованы в SVG: контейнеровоз, балкер, нефтевоз, химовоз, газовоз, генгруз, ро-ро. Какая показывается, зависит от поля «Иллюстрация» у типа судна.
- В админке у вакансии можно загрузить **своё фото судна** — оно заменит иллюстрацию.
- Для страниц моряка и судовладельца: `seafarer.svg`, `shipowner.svg` — их тоже можно заменить на свои файлы с теми же именами.
- Для загруженных фото нужен Pillow (уже в `requirements.txt`).
