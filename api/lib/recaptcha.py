from config import recaptcha_secret
import requests

_session = requests.session()
def validate_recaptcha(response, remote_ip='') -> bool:
    if not recaptcha_secret:
        return True
    try:
        res = _session.post("https://www.google.com/recaptcha/api/siteverify", data={
            'secret': recaptcha_secret, 
            'response': response,
            'remoteip': remote_ip})
        data = res.json()
        return data['success']
    except Exception as e:
        print('recaptcha error:', e)
        return False