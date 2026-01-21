Run command

uvicorn app.main:app --reload


alembic revision --autogenerate -m "command"
alembic upgrade head
