"""
Gunicorn config for Railway. Binds to PORT from environment.
"""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = 1
threads = 2
timeout = 60
forwarded_allow_ips = "*"
