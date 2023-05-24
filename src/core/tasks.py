from django.core.mail import send_mail
from kavenegar import *


def send_opt_sms(code: str):
    try:
        api = KavenegarAPI('7A51505630436F50615247437A64326E3564524439413262354E6A6246344E39412B573530764863327A6F3D')
        params = {'sender': '1000596446', 'receptor': '09128145528', 'message': f'{code}.وب سرویس پیام کوتاه کاوه نگار'}
        response = api.sms_send(params)
        print(response)
    except (APIException, HTTPException) as e:
        print(e)


def send_opt_email(code: str, email: str):
    send_mail("Email Verification", f"hi. Your verification code is {code}",
              'smrazavi19911370@gmail.com', email)
