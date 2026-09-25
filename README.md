# BioFlora — цветочный магазин на Django

Готовый учебный интернет-магазин цветов на Django.

## Возможности
- каталог цветов;
- категории;
- карточки товаров с изображениями;
- поиск;
- корзина на сессии;
- оформление заказа;
- административная панель Django;
- адаптивный дизайн без внешних CSS-фреймворков.

## Запуск

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

Для админки:
```bash
python manage.py createsuperuser
```

Затем http://127.0.0.1:8000/admin/

Данные демо-магазина создаются командой `seed_demo`.
