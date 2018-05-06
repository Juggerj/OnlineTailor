#-*- coding: utf-8 -*-
from django import forms
from app.models import Customer

class MainForm(forms.Form):
    # class Meta:
    #    model = Customer
    #    fields = ['name', 'email', 'phone']

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    email = forms.EmailField(max_length= 100,
                              widget=forms.TextInput(attrs={'placeholder': 'Ваш Email',
                                                            'pattern': '^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$',
                                                            'title': 'Вы неверно ввели номер мобильного телефона, повторите ввод в формате info@gmail.com'}))
    phone = forms.CharField(max_length= 100,
                              widget=forms.TextInput(attrs={'placeholder': 'Ваш номер телефона',
                                                            'pattern': '^8\(\d{3}\)\d{3}-\d{2}-\d{2}$',
                                                            'id': 'phone',
                                                            'title': 'Введите номер телефона'}))

