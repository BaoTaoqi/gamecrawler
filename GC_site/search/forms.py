from django import forms


class SteamSearchForm(forms.Form):
    text = forms.CharField(label='搜索内容', max_length=200)