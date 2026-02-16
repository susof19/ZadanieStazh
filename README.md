# Рецепты — REST API

Небольшой API для рецептов на FastAPI + SQLAlchemy + SQLite.

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Приложение: http://127.0.0.1:8000  
Документация API: http://127.0.0.1:8000/docs  

## Готовность:

| Требование | Статус |
|------------|--------|
| Модель: id, title, ingredients, steps, tags, created_at | Готово |
| CRUD (создание, получение, обновление, удаление) | Готово |
| Фильтрация по тегу | Готово |
| Фильтрация по ингредиенту | Готово |
| Валидация (title, ingredients, steps не пустые) | Готово |
| HTTP-коды 200, 201, 404 | Готово |
| FastAPI, Pydantic, SQLAlchemy, SQLite | Готово |
| Структура: модели, crud, маршруты | Готово |
| Ruff (все правила) | Проходит |
| ty (type checker) | Проходит |
| Тесты pytest | Тест пройден успешно |
