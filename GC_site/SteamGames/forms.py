from django import forms
from captcha.fields import CaptchaField


class SubscribeForm(forms.Form):
    captcha = CaptchaField(label='确认码', error_messages={"invalid": "确认码错误!"})
