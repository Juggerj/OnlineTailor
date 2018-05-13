#-*- coding: utf-8 -*-

from random import randint
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.context_processors import csrf
from db.models import *
from app.models import *
from app.views import order,preOrder
from app.forms import PrePaymentForm
from forms import *
import json


from django.core.mail import send_mail
import re

def Sender(adr,code,address):
    print 'send mail'
    send_mail(u'Подтверждение подски ' + address,
              u'Здравствуйте!\nДля подтверждения подписки пройдите по ссылке ниже:\n\nhttp://'+address+'/submit/'+str(code),
              'Inform@shit-modno.ru',
              [adr] )

def load_content():
    Pic = {}
    pics = Picture.objects.filter()
    for i in xrange(len(pics)):
        if pics[i].block.short_name not in Pic.keys():
            Pic[pics[i].block.short_name] = {}

        if pics[i].short_name not in Pic[pics[i].block.short_name].keys():
            Pic[pics[i].block.short_name][pics[i].short_name] = pics[i]
        else:
            # print type(Pic[pics[i].block.short_name][pics[i].short_name])
            if isinstance(Pic[pics[i].block.short_name][pics[i].short_name], Picture):
                tmp = Pic[pics[i].block.short_name][pics[i].short_name]
                Pic[pics[i].block.short_name][pics[i].short_name] = [tmp, pics[i]]
            else:
                Pic[pics[i].block.short_name][pics[i].short_name].append(pics[i])

    Art = {}
    arts = Article.objects.filter().order_by('block','short_name','ord')
    for i in xrange(len(arts)):
        # если нет такого блока - добавь
        if arts[i].block.short_name not in Art.keys():
            Art[arts[i].block.short_name] = {}
        # если нет такого подблока - добавь и сунь ему один конкретный элемент иначе проверь массив
        if arts[i].short_name not in Art[arts[i].block.short_name].keys():
            Art[arts[i].block.short_name][arts[i].short_name] = arts[i].content
        else:
            if isinstance(Art[arts[i].block.short_name][arts[i].short_name], basestring):
                tmp = Art[arts[i].block.short_name][arts[i].short_name]
                Art[arts[i].block.short_name][arts[i].short_name] = [tmp, arts[i].content]
            else:
                Art[arts[i].block.short_name][arts[i].short_name].append(arts[i].content)

    good = Goods.objects.get_or_create(name__exact = Art['Offer']['Maximum'][0])

    Art['Offer']['Maximum'].append(str(good[0].price) + ' рублей')
    Art['Offer']['Maximum_good'] = good[0].id

    good = Goods.objects.get_or_create(name__exact = Art['Offer']['Standart'][0])

    Art['Offer']['Standart'].append(str(good[0].price) + ' рублей')
    Art['Offer']['Standart_good'] = good[0].id

    good = Goods.objects.get_or_create(name__exact = Art['Offer']['Minimal'][0])

    Art['Offer']['Minimal'].append(str(good[0].price) + ' рублей')
    Art['Offer']['Minimal_good'] = good[0].id

    DependArt = {}

    DependArt['Questions'] = []
    for i in xrange(len(Art['Questions']['Question'])):
        DependArt['Questions'].append({'ord': i, 'items': [Art['Questions']['Question'][i], Art['Questions']['Answer'][i]]})

    DependArt['Topics'] = []

    topics = Article.objects.filter(short_name__exact='Topic',block__exact=Block.objects.filter(short_name__exact = 'Program')).order_by('ord')


    for item in topics:
        # print item.ord, item.content

        subtopics = Article.objects.filter(short_name__exact = 'Subtopic', ord__exact = item.ord,
                                           block__exact = Block.objects.filter(short_name__exact = 'Program').order_by('content'))
        DependArt['Topics'].append({'theme':item.content,'items':[x.content for x in subtopics]})

    return Pic,Art,DependArt

@csrf_exempt
def index(request):

    Pic,Art,DependArt = load_content()

    abouts = Visitor.objects.filter()

    address = 'made-fashion.ru'

    if 'user_id' in request.COOKIES:
        try:
            customer = Customer.objects.get(id=request.COOKIES['user_id'])

            subscribtion_form = MainForm(initial={'name': customer.name,
                                                  'phone': customer.phone,
                                                  'email': customer.email})

            print customer.name
        except:
            subscribtion_form = MainForm()
    else:
        subscribtion_form = MainForm()


    return render_to_response('index.html',locals())

def schedule(request):

    Pic,Art,DependArt = load_content()

    return render_to_response('schedule.html',locals())

def offer(request):

    Pic,Art,DependArt = load_content()

    return render_to_response('offer.html',locals())

def recall_base(request, id, cur_id):
    """
    Возвращает заполненную форму для редактирования Пользователя(User) с заданным user_id
    """
    pics = Picture.objects.filter(block__exact = Block.objects.filter(short_name__exact = 'Recalls')[0].id)

    arts = Article.objects.filter(short_name__exact = 'recall', block__exact = Block.objects.filter(short_name__exact = 'Recalls')[0].id)

    res = [int(cur_id) + int(id) - 1, int(cur_id) + int(id), int(cur_id) + int(id) + 1]

    if res[1] < 0:
        res[1] = len(pics)-1
        res[0] = len(pics)-2
    elif res[0] < 0:
        res[0] = len(pics)-1

    if res[1] > len(pics)-1:
        res[1] = 0
        res[2] = 1
    elif res[2] > len(pics)-1:
        res[2] = 0

    # print res

    if request.is_ajax():

        context = {'left': pics[res[0]],
                   'main': pics[res[1]],
                   'right': pics[res[2]],
                   'cur': res[1],
                   'name': arts[res[1]].content}
        # recalls.update(csrf(request))
        html = loader.render_to_string('blocks/recalls_base.html', context)
        data = {'errors': False, 'html': html}
        return JsonResponse(data)

@csrf_exempt
def catch_visitor(request):
    context = {}
    context.update(csrf(request))
    if request.is_ajax():
        if request.method == 'POST':
            try:
                src = re.search('://((\w|[^/])*)/',request.POST.dict()['ref']).group(1)
            except:
                src = 'Прямой вход'
            try:
                item = Visitor(remote_adr = request.POST.dict()['addr'],
                               city = request.POST.dict()['city'],
                               region = request.POST.dict()['region'],
                               time_zone = request.POST.dict()['time_zone'],
                               refer = request.POST.dict()['ref'],
                               browser = request.POST.dict()['browser'],
                               version = request.POST.dict()['version'],
                               device = request.POST.dict()['device'],
                               os = request.POST.dict()['os'],
                               time = timezone.now(),
                               source = src)
                item.save()
            except:
                pass

        html = loader.render_to_string('index.html', context)
        data = {'errors': False, 'html':html}
        return JsonResponse(data)

@csrf_exempt
def subscription(request):

    Pic,Art,DependArt = load_content()

    abouts = Visitor.objects.filter()

    address = 'made-fashion.ru'

    if request.method == 'POST':
        subscribtion_form = MainForm(request.POST)

        if subscribtion_form.is_valid():

            try:
                customer = Customer.objects.get_or_create(name=subscribtion_form.cleaned_data['name'],
                                                          email=subscribtion_form.cleaned_data['email'],
                                                          phone=subscribtion_form.cleaned_data['phone'])[0]


                c_code = u''
                for y in [str(randint(0, 9)) for x in range(50)]:
                    c_code += y

                p = Lead.objects.create(type=Lead.LEAD_TYPE.SUBSCRIBE_TRY,
                                        customer_id=customer,
                                        auth_code=c_code)
                p.save()
                # Sender(customer.email,c_code,address)

                response = render_to_response('subscription.html',locals())
                response.set_cookie( 'user_id', customer.id)
            except:
                response = render_to_response('subscription.html',locals())
    else:
        response = render_to_response('index.html',locals())

    return response

@csrf_exempt
def order_page(request, id):
    Pic,Art,DependArt = load_content()

    method = request.method

    if request.method == 'GET':
        form = preOrder(id, request.COOKIES)
        response = render_to_response('order_page.html', locals())


    else:
        preOrderForm = PrePaymentForm(request.POST, request.COOKIES)

        if preOrderForm.is_valid():

            ym_merchant = {"customerContact": preOrderForm.cleaned_data['email'],
                   "taxSystem": '6',
                   "items": [{"quantity": 1,
                             "price": {"amount": preOrderForm.cleaned_data['sum']},
                             "tax": 1,
                             "text": preOrderForm.cleaned_data['good']},]}

            dt={'id':id,
                'name': preOrderForm.cleaned_data['name'],
                'email': preOrderForm.cleaned_data['email'],
                'phone': preOrderForm.cleaned_data['phone'],
                'ym_merchant_receipt':json.dumps(ym_merchant)}
            print dt
            customer_id,form = order(dt)

        response = render_to_response('order_page.html', locals())
        response.set_cookie( 'user_id', customer_id)

    return response


def submit(request, auth_code):

    Pic,Art,DependArt = load_content()

    p = Lead.objects.filter(auth_code=auth_code).update(type = Lead.LEAD_TYPE.SUBSCRIBE)

    return render_to_response('submit.html',locals())

