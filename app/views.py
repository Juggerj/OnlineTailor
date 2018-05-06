# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from forms import PaymentForm, PrePaymentForm
from django.utils import timezone
from datetime import timedelta
import json


def order(spisok):

    good = Goods.objects.get_or_create(id = spisok['id'])[0]

    customer = Customer.objects.get_or_create(name=spisok['name'],
                                              email=spisok['email'],
                                              phone=spisok['phone'])[0]

    customer.save()


    payment = Payments(order_amount=good.price,
                       cps_email=spisok['email'],
                       cps_phone=spisok['phone'],
                       good_id=good,
                       customer_id=customer,
                       customer_number=customer.id,
                       order_number=Payments.objects.latest('id').id + 1,
                       ym_merchant_receipt=spisok['ym_merchant_receipt'])
    payment.save()

    p = Lead.objects.create(type=Lead.LEAD_TYPE.PURCHASE,
                            customer_id=customer,
                            payment_id=payment)
    p.save()

    form = PaymentForm(instance=payment)

    return customer.id, form

def preOrder(id, cookies):

    goods = Goods.objects.get_or_create(id = id)[0]

    if 'user_id' in cookies:
        try:
            customer = Customer.objects.get(id = cookies['user_id'])
            form = PrePaymentForm(initial={'good': goods.name,
                                           'sum': goods.price,
                                           'name': customer.name,
                                           'phone': customer.phone,
                                           'email': customer.email})
        except:
            form = PrePaymentForm(initial={'good':goods.name, 'sum':goods.price})
    else:
        form = PrePaymentForm(initial={'good':goods.name, 'sum':goods.price})

    return form

@csrf_exempt
def aviso(request):

    if request.method == 'POST':

        performedDatetime = timezone.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]+'+00:00'
        invoiceId = request.POST.dict()['invoiceId']
        shopId = request.POST.dict()['shopId']

        code = 0

        for item in request.POST:
            print [item, request.POST[item]]

        try:
            payment = Payments.objects.filter(customer_number=request.POST['customerNumber'],
                      order_number=request.POST['orderNumber']).update(status='success',
                                                                       payment_type=request.POST['paymentType'])
            payment.save()
        except:
            pass

    return render_to_response('payments/aviso.html',locals())

@csrf_exempt
def check(request):

    if request.method == 'POST':
        performedDatetime = timezone.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]+'+00:00'
        invoiceId = request.POST.dict()['invoiceId']
        shopId = request.POST.dict()['shopId']


        payment = Payments.objects.filter(customer_number=request.POST['customerNumber'],
                                          order_number=request.POST['orderNumber'])[0]

        if payment.performed_datetime > timezone.now() - timedelta(1):
            code = 0
        else:
            code = 1

        try:
            payment = Payments.objects.filter(customer_number=request.POST['customerNumber'],
                      order_number=request.POST['orderNumber']).update(status='checked',
                                                                       invoice_id=invoiceId)
            payment.save()
        except:
            pass


    return render_to_response('payments/check.html',locals())

@csrf_exempt
def success(request):

    params = []
    if request.method == 'GET':
        for item in request.GET:
            params.append([item, request.GET[item]])

    return render_to_response('payments/success.html',locals())

@csrf_exempt
def fail(request):

    params = []
    if request.method == 'GET':
        for item in request.GET:
            params.append([item, request.GET[item]])

    try:
        payment = Payments.objects.filter(customer_number=request.POST['customerNumber'],
                  order_number=request.POST['orderNumber']).update(status='fail')
        payment.save()
    except:
        pass


    return render_to_response('payments/fail.html',locals())

@csrf_exempt
def processed(request):

    if request.method == 'POST':

        payment = Payments.objects.filter(customer_number=request.POST['customerNumber'],
                  order_number=request.POST['orderNumber']).update(cps_email=request.POST['cps_email'],cps_phone=request.POST['cps_phone'])


    return render_to_response('payments/processed.html',locals())