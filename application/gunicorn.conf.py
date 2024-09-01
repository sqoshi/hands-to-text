# import multiprocessing

workers = 3  # Adjust based on your needs
worker_class = "sync"  # Change as needed
max_requests = 1000
timeout = 60
worker_timeout = 60
accesslog = "-"  # Use stdout for logs
errorlog = "-"  # Use stderr for logs
bind = "0.0.0.0:8001"
graceful_timeout = 30

# Access log format (same as Flask's log format for consistency)
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
