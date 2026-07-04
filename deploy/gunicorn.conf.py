"""Gunicorn configuration.

Bind defaults to TCP for Docker; systemd overrides GUNICORN_BIND to a unix socket.
Worker count is kept low by default for shared hosting with limited NPROC.
"""
import multiprocessing
import os

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
workers = int(os.environ.get('GUNICORN_WORKERS', min(multiprocessing.cpu_count() * 2 + 1, 4)))
threads = int(os.environ.get('GUNICORN_THREADS', 2))
timeout = 60
graceful_timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100

accesslog = os.environ.get('GUNICORN_ACCESS_LOG', '-')
errorlog = os.environ.get('GUNICORN_ERROR_LOG', '-')
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')
