import os
from celery import Celery
# import time
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ustora.settings')
# app = Celery('ustora', backend='rpc://', broker='pyamqp://guest@localhost//') , backend='rpc://', broker='amqp://guest@localhost//'
app = Celery('ustora')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
