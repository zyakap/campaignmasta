import multiprocessing

bind = "unix:/run/campaignmasta.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
accesslog = "/var/log/gunicorn/campaignmasta-access.log"
errorlog = "/var/log/gunicorn/campaignmasta-error.log"
loglevel = "info"
