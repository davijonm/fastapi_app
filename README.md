1. chmod +x backend/start.sh
2. docker compose build -d && docker compose up
3. docker compose exec alembic revision --autogenerate -m "Initial migration" 
4. docker compose exec alembic upgrade head
