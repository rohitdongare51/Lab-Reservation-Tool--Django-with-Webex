import time
from .models import Testbed
import requests
import datetime
from django.utils import timezone
from .constants import users, send_webex_message

druva='Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jOWU2YjkzMi02OTMwLTQyMTktOWMzMi02MDg0NGZkYjVjZTY'
rdongare='Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iZDViMjAyOC1kNjk4LTQwYjUtYTdmMC1jNzQzNDg3YzkxNjU'
# users = {'druva': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jOWU2YjkzMi02OTMwLTQyMTktOWMzMi02MDg0NGZkYjVjZTY',
#         'rdongare': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iZDViMjAyOC1kNjk4LTQwYjUtYTdmMC1jNzQzNDg3YzkxNjU'}
def my_cron_job():

    headers={'Authorization': 'Bearer OGNkNjAyZmMtMjMwOC00N2IwLWJmMWEtZTVlNThiOWJjYjM1Y2I1NjkxMjctZWNh_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f', 'Content-type': 'application/json;charset=utf-8'}
   
    devices = Testbed.objects.filter(usage='notfree',device_type='ftd') | Testbed.objects.filter(usage='notfree',device_type='fmc')
    in_use_one_week = []
    current_time = datetime.datetime.now(timezone.utc)
    for device in devices:
        delta_time = current_time - device.date_posted
        print(device, delta_time.seconds, delta_time.seconds > 3600)
        if delta_time.seconds > 3600:

            send_webex_message(True,device.testbed_uploader.username,device.device,sending_user=None)
