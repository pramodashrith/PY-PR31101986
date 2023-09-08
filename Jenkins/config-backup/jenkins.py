from http import server
import imp
import jenkins
import json
import os
from importlib import import_module
from api4jenkins import Jenkins


host = "http://localhost:8080"
username = "admin"
password = "admin"
j = Jenkins('http://127.0.0.1:8080/', auth=('admin', 'admin'))
for job in j.iter_jobs(depth=8):
    print(job)
# job = j.get_job('pipeline')
# j.version
# print(j)
# print(job)



