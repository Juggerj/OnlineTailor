# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
#
from hashlib import md5

import six
from django.conf import settings
from models import Payments


class PrePaymentForm(forms.Form):

    good = forms.CharField(label='Услуга',
                           required=True,
                           widget=forms.TextInput(attrs={'readonly': '1'}))
    sum = forms.FloatField(label='Стоимость, руб',
                           required=True,
                           widget=forms.TextInput(attrs={'readonly': '1'}))

    name = forms.CharField(label='ФИО',
                           required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Фамилия Имя Отчество'}))
    email = forms.EmailField(label = 'Email',
                             max_length= 100,
                             required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Ваш Email',
                                                           'pattern': '^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$',
                                                           'title': 'Вы неверно ввели номер мобильного телефона, повторите ввод в формате info@gmail.com'}))
    phone = forms.CharField(label = 'Номер телефона',
                            max_length= 100,
                            required=True,
                            widget=forms.TextInput(attrs={'placeholder': '8(XXX)XXX-XX-XX',
                                                          'pattern': '^8\(\d{3}\)\d{3}-\d{2}-\d{2}$',
                                                          'id': 'phone',
                                                          'title': 'Введите номер телефона'}))

    # paymentType = forms.CharField(label='Способ оплаты',
    #                               widget=forms.Select(choices=Payments.PAYMENT_TYPE.CHOICES),
    #                               min_length=2, max_length=2,
    #                               initial=Payments.PAYMENT_TYPE.AC)

class BasePaymentForm(forms.Form):
    """
        shopArticleId               <no use>
        scid                        scid
        sum                         amount
        customerNumber              user
        orderNumber                 id
        shopSuccessURL              success_url
        shopFailURL                 fail_url
        cps_provider                payment_type
        cps_email                   cps_email
        cps_phone                   cps_phone
        paymentType                 payment_type
        shopId                      shop_id
        invoiceId                   invoice_id
        orderCreatedDatetime        <no use>
        orderSumAmount              order_amount
        orderSumCurrencyPaycash     order_currency
        orderSumBankPaycash         <no use>
        shopSumAmount               shop_amount
        shopSumCurrencyPaycash      shop_currency
        shopSumBankPaycash          <no use>
        paymentPayerCode            payer_code
        paymentDatetime             <no use>
        cms_name                    django
    """

    class ERROR_MESSAGE_CODES:
        BAD_SCID = 0
        BAD_SHOP_ID = 1

    error_messages = {
        ERROR_MESSAGE_CODES.BAD_SCID: 'scid не совпадает с YANDEX_MONEY_SCID',
        ERROR_MESSAGE_CODES.BAD_SHOP_ID: 'scid не совпадает с YANDEX_MONEY_SHOP_ID'
    }

    class ACTION:
        CHECK = 'checkOrder'
        CPAYMENT = 'paymentAviso'

        CHOICES = (
            (CHECK, 'Проверка заказа'),
            (CPAYMENT, 'Уведомления о переводе'),
        )

    shopId = forms.IntegerField(initial=settings.YANDEX_MONEY_SHOP_ID)
    scid = forms.IntegerField(initial=settings.YANDEX_MONEY_SCID)
    orderNumber = forms.CharField(min_length=1, max_length=64)
    customerNumber = forms.CharField(min_length=1, max_length=64)
    # paymentType = forms.CharField(label='Способ оплаты',
    #                               widget=forms.Select(choices=Payments.PAYMENT_TYPE.CHOICES),
    #                               min_length=2, max_length=2,
    #                               initial=Payments.PAYMENT_TYPE.AC)
    orderSumBankPaycash = forms.IntegerField()

    md5 = forms.CharField(min_length=32, max_length=32)
    action = forms.CharField(max_length=16)
    ym_merchant_receipt = forms.CharField(max_length=2000)

    def __init__(self, *args, **kwargs):
        super(BasePaymentForm, self).__init__(*args, **kwargs)
        if hasattr(settings, 'YANDEX_ALLOWED_PAYMENT_TYPES'):
            allowed_payment_types = settings.YANDEX_ALLOWED_PAYMENT_TYPES
            # self.fields['paymentType'].widget.choices = filter(
            #     lambda x: x[0] in allowed_payment_types,
            #     self.fields['paymentType'].widget.choices)

    @classmethod
    def make_md5(cls, cd):
        """
        action;orderSumAmount;orderSumCurrencyPaycash;orderSumBankPaycash;shopId;invoiceId;customerNumber;shopPassword
        """
        return md5(';'.join(map(six.text_type, (
            cd['action'],
            cd['orderSumAmount'],
            cd['orderSumCurrencyPaycash'],
            cd['orderSumBankPaycash'],
            cd['shopId'],
            cd['invoiceId'],
            cd['customerNumber'],
            settings.YANDEX_MONEY_SHOP_PASSWORD,
        ))).encode('utf-8')).hexdigest().upper()

    @classmethod
    def check_md5(cls, cd):
        return cls.make_md5(cd) == cd['md5']

    def clean_scid(self):
        scid = self.cleaned_data['scid']
        if (
            scid != settings.YANDEX_MONEY_SCID and
            not scid in Payments.get_used_scids()
        ):
            raise forms.ValidationError(self.error_messages[self.ERROR_MESSAGE_CODES.BAD_SCID])
        return scid

    def clean_shopId(self):
        shop_id = self.cleaned_data['shopId']
        if (
            shop_id != settings.YANDEX_MONEY_SHOP_ID and
            not shop_id in Payments.get_used_shop_ids()
        ):
            raise forms.ValidationError(self.error_messages[self.ERROR_MESSAGE_CODES.BAD_SHOP_ID])
        return shop_id


class PaymentForm(BasePaymentForm):
    sum = forms.FloatField(label='Сумма заказа')

    cps_email = forms.EmailField(label='Email', required=False)
    cps_phone = forms.CharField(label='Телефон', max_length=15, required=False)

    shopFailURL = forms.URLField(initial=settings.YANDEX_MONEY_FAIL_URL)
    shopSuccessURL = forms.URLField(initial=settings.YANDEX_MONEY_SUCCESS_URL)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        super(PaymentForm, self).__init__(*args, **kwargs)

        self.fields.pop('md5')
        self.fields.pop('action')
        self.fields.pop('orderSumBankPaycash')

        if not getattr(settings, 'YANDEX_MONEY_DEBUG', False):
            for name in self.fields:
                if name not in self.get_display_field_names():
                    self.fields[name].widget = forms.HiddenInput()

        if instance:
            self.fields['sum'].initial = instance.order_amount
            # self.fields['paymentType'].initial = instance.payment_type
            self.fields['customerNumber'].initial = instance.customer_number
            self.fields['orderNumber'].initial = instance.order_number
            if instance.fail_url:
                self.fields['shopFailURL'].initial = instance.fail_url
            if instance.success_url:
                self.fields['shopSuccessURL'].initial = instance.success_url
            if instance.cps_email:
                self.fields['cps_email'].initial = instance.cps_email
            if instance.cps_phone:
                self.fields['cps_phone'].initial = instance.cps_phone
            if instance.ym_merchant_receipt:
                self.fields['ym_merchant_receipt'].initial = instance.ym_merchant_receipt

    def get_display_field_names(self):
        return [ 'cps_email', 'cps_phone']


class CheckForm(BasePaymentForm):
    invoiceId = forms.IntegerField()
    orderSumAmount = forms.DecimalField(min_value=0, decimal_places=2)
    orderSumCurrencyPaycash = forms.IntegerField()
    shopSumAmount = forms.DecimalField(min_value=0, decimal_places=2)
    shopSumCurrencyPaycash = forms.IntegerField()
    paymentPayerCode = forms.IntegerField(min_value=1, required=False)


class NoticeForm(BasePaymentForm):
    invoiceId = forms.IntegerField(min_value=1)
    orderSumAmount = forms.DecimalField(min_value=0, decimal_places=2)
    orderSumCurrencyPaycash = forms.IntegerField()
    shopSumAmount = forms.DecimalField(min_value=0, decimal_places=2)
    shopSumCurrencyPaycash = forms.IntegerField()
    paymentPayerCode = forms.IntegerField(min_value=1, required=False)
    cps_email = forms.EmailField(required=False)
    cps_phone = forms.CharField(max_length=15, required=False)
