from django.core.mail import send_mail
from kavenegar import *
import random
import redis
from celery import shared_task


@shared_task
def send_opt_sms(phone: str, expiry_time: int):
    try:
        code = random.randint(100000, 999999)
        api = KavenegarAPI('7A51505630436F50615247437A64326E3564524439413262354E6A6246344E39412B573530764863327A6F3D')
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.setex(phone, expiry_time, str(code))
        params = {'sender': '1000596446', 'receptor': phone, 'message': f'{code}.وب سرویس پیام کوتاه کاوه نگار'}
        response = api.sms_send(params)
        print(response)
    except (APIException, HTTPException) as e:
        print(e)


@shared_task
def send_opt_email(email: str, expiry_time: int):
    code = random.randint(100000, 999999)
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.setex(email, expiry_time, str(code))
    send_mail("Email Verification", f"hi. Your verification code is {code}",
              'smrazavi19911370@gmail.com', (email,))
