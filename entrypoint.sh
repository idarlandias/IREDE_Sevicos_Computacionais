# Start Cron service
service cron start

# Start Nginx in background
nginx &

# Start FastAPI app
uvicorn app.main:app --host 0.0.0.0 --port 8000
