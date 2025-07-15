# gunicorn_conf.py
bind = "0.0.0.0:8000"
workers = 4 # the number of workers depends on the number of CPU cores
worker_class = "uvicorn.workers.UvicornWorker"
