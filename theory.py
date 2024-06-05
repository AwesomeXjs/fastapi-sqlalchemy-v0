# pip install fastapi uvicorn[standart]

# poetry - система контроля зависимостей
# poetry init - инициализация текущего проекта
# poetry new name - создание нового проекта и инициализация
# poetry install - установка вписаных зависимостей
# poetry install --sync - синхронизирует текущее окружение с тем что нужно установить
# poetry update fastapi - обновление конкретной зависимости
# poetry add - добавление к текущим зависимостям нового
# poetry show --tree - список зависимостей


# CRUD - Create Read Update Delete

# работа с алхимией:
# инициализация fastapi =>
# 1. settings
# 2. db_helper для всех подключений
# 3. модели
# 4. alembic создание миграций и создание первых таблиц
# 5. создание schemas > crud > views

# alembic запросы
# alembic init alembic (для асинхронки alembic init -t async alembic)
# alembic revision --autogenerate -m "create revision"
# alembic upgrade head (к последней версии) (до определенной версии указать хэш ревизии вместо head)
# alembic downgrade -1 (откатить последнюю версию) (или определенную по хэшу)
# alembic history - полказывает историю миграций
# alembic current - показывает текущую миграцию


# Виды запросов:

# default:

# @app.get('/')
# def get_home():
#     return {'status': 200, 'data': 'Hello World'}


# query params:

# @app.get('/hello')
# def get_hello(name: str = 'Dima'):  # query params
#     name = name.strip().title()
#     return {'message': f"Hello {name}"}


# path params

# @app.get('/items/{item_id}/')
# def get_item_by_id(item_id:int):  # path params
#     return {
#         "item": {
#             'id': item_id
#         }
#     }
