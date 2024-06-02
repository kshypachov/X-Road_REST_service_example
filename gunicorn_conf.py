# gunicorn_conf.py
bind = "0.0.0.0:8000"
workers = 4  # кількість воркерів залежить від кількості ядер процесора
worker_class = "uvicorn.workers.UvicornWorker"
