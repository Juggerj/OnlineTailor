# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from uuid import uuid4
import six
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import Signal

payment_process = Signal()
payment_completed = Signal()


def get_default_as_uuid():
    return six.text_type(uuid4()).replace('-', '')


class Customer(models.Model):
  name = models.CharField(verbose_name='ФИО', max_length=191, blank=True, null=False)
  phone = models.CharField(verbose_name='Телефон', max_length=15, blank=True, null=False)
  email = models.EmailField(verbose_name='Email', max_length=100, blank=True, null=False)

  def __unicode__(self):
        return self.name

  class Meta:
        ordering = ('-id',)
        unique_together = (
            ('name', 'email', 'phone'),
        )
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

class Goods(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=32)
    price = models.PositiveIntegerField(verbose_name='Стоимость')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Payments(models.Model):
    class STATUS:
        PROCESSED = 'processed'
        CHECKED_S = 'checked_s'
        CHECKED_F = 'checked_f'
        SUCCESS = 'success'
        FAIL = 'fail'

        CHOICES = (
            (PROCESSED, 'Счет выставлен'),
            (CHECKED_S, 'Проверка пройдена'),
            (CHECKED_F, 'Проверка не пройдена  '),
            (SUCCESS, 'Счет оплачен'),
            (FAIL, 'Счет не оплачен'),
        )

    class PAYMENT_TYPE:
        AC = 'AC'
        PC = 'PC'
        GP = 'GP'
        MC = 'MC'
        WM = 'WM'
        SB = 'SB'
        AB = 'AB'
        MA = 'MA'
        PB = 'PB'
        QW = 'QW'
        QP = 'QP'
        DF = 'DF'

        CHOICES = (
            (PC, 'Кошелек Яндекс.Деньги'),
            (AC, 'Банковская карта'),
            (GP, 'Наличными через кассы и терминалы'),
            (MC, 'Счет мобильного телефона'),
            (WM, 'Кошелек WebMoney'),
            (SB, 'Сбербанк: оплата по SMS или Сбербанк Онлайн'),
            (AB, 'Альфа-Клик'),
            (MA, 'MasterPass'),
            (PB, 'Интернет-банк Промсвязьбанка'),
            (QW, 'QIWI Wallet'),
            (QP, 'Доверительный платеж (Куппи.ру)'),
            (DF, 'Не выбран'),
        )

    class CURRENCY:
        RUB = 643
        TEST = 10643

        CHOICES = (
            (RUB, 'Рубли'),
            (TEST, 'Тестовая валюта'),
        )

    customer_id = models.ForeignKey(Customer, verbose_name='Покупатель', blank=True, null= True)

    good_id = models.ForeignKey(Goods, verbose_name='Товар', blank=True, null= True)

    pub_date = models.DateTimeField('Время создания', auto_now_add=True)

    # Required request fields
    shop_id = models.PositiveIntegerField(
        'ID магазина', default=settings.YANDEX_MONEY_SHOP_ID)
    scid = models.PositiveIntegerField(
        'Номер витрины', default=settings.YANDEX_MONEY_SCID)
    customer_number = models.CharField(
        'Идентификатор плательщика', max_length=64,
        default=get_default_as_uuid)
    order_amount = models.DecimalField(
        'Сумма заказа', max_digits=15, decimal_places=2)

    # Non-required fields
    payment_type = models.CharField(
        'Способ платежа', max_length=2, default=PAYMENT_TYPE.DF,
        choices=PAYMENT_TYPE.CHOICES)
    order_number = models.CharField(
        'Номер заказа', max_length=64,
        default=get_default_as_uuid)
    cps_email = models.EmailField(
        'Email плательщика', max_length=100, blank=True, null=True)
    cps_phone = models.CharField(
        'Телефон плательщика', max_length=15, blank=True, null=True)
    success_url = models.URLField(
        'URL успешной оплаты', default=settings.YANDEX_MONEY_SUCCESS_URL)
    fail_url = models.URLField(
        'URL неуспешной оплаты', default=settings.YANDEX_MONEY_FAIL_URL)

    # Transaction info
    status = models.CharField(
        'Статус', max_length=16, choices=STATUS.CHOICES,
        default=STATUS.PROCESSED)
    invoice_id = models.PositiveIntegerField(
        'Номер транзакции оператора', blank=True, null=True)
    shop_amount = models.DecimalField(
        'Сумма полученная на р/с', max_digits=15, decimal_places=2, blank=True,
        null=True, help_text='За вычетом процента оператора')
    order_currency = models.PositiveIntegerField(
        'Валюта', default=CURRENCY.RUB, choices=CURRENCY.CHOICES)
    shop_currency = models.PositiveIntegerField(
        'Валюта полученная на р/с', blank=True, null=True,
        default=CURRENCY.RUB, choices=CURRENCY.CHOICES)
    performed_datetime = models.DateTimeField(
        'Время выполнение запроса',default = timezone.now(), blank=True, null=True)

    ym_merchant_receipt = models.TextField('Корзина', max_length=2000, blank=True, null=True)

    @property
    def is_payed(self):
        return self.status == self.STATUS.SUCCESS

    def send_signals(self):
        status = self.status
        if status == self.STATUS.PROCESSED:
            payment_process.send(sender=self)
        if status == self.STATUS.SUCCESS:
            payment_completed.send(sender=self)

    @classmethod
    def get_used_shop_ids(cls):
        return cls.objects.values_list('shop_id', flat=True).distinct()

    @classmethod
    def get_used_scids(cls):
        return cls.objects.values_list('scid', flat=True).distinct()

    class Meta:
        ordering = ('-pub_date',)
        unique_together = (
            ('shop_id', 'order_number'),
        )
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return u'Сумма: {}, Статус:{}'.format(self.order_amount, self.get_status_display())


class Lead(models.Model):
    class LEAD_TYPE:
        SUBSCRIBE_TRY = 'try_subscribe'
        SUBSCRIBE = 'subscribe'
        UNSUBSCRIBE = 'unsubscribe'
        PURCHASE = 'purchase'

        CHOICES = (
            (SUBSCRIBE_TRY, u'Подписка, не подтвердена'),
            (SUBSCRIBE, u'Подписка, подтверждена'),
            (UNSUBSCRIBE, u'Подписка, отменена'),
            (PURCHASE, u'Покупка'),
        )

    time = models.DateTimeField(default = timezone.now(),verbose_name='Дата оставления заявки')
    type = models.CharField(max_length=50,default='',verbose_name='Тип заявки',choices=LEAD_TYPE.CHOICES, blank=True, null= True)
    customer_id = models.ForeignKey(Customer, verbose_name='Покупатель', blank=True, null= True)
    payment_id = models.ForeignKey(Payments, verbose_name='Платеж', blank=True, null= True)
    auth_code = models.CharField(max_length=50, default=u'0', verbose_name='Код авторизации')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
