#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class Block(models.Model):
    short_name = models.CharField(max_length=200,default='', verbose_name= 'Краткое описание (англ без пробелов)', blank=True, null=True)
    full_name = models.CharField(max_length=200,default='', verbose_name= 'Полное описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'
    def __unicode__(self):
        return '%s' % (self.full_name)

class Article(models.Model):
    short_name = models.CharField(max_length=200,default='', verbose_name= 'Краткое описание', blank=True, null=True)
    content = models.TextField(max_length=5000,default='', verbose_name= 'Контент', blank=True, null=True)
    ord = models.IntegerField(default=0, verbose_name= 'Порядковый номер')
    block = models.ForeignKey(Block,default='',verbose_name= 'Блок', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    def __unicode__(self):
        return str(self.ord) + ' || ' + self.block.short_name + ' || ' + self.short_name

class Picture(models.Model):

    short_name = models.CharField(max_length=200,default='', verbose_name= 'Краткое описание', blank=True, null=True)
    description = models.TextField(max_length=5000,default='', verbose_name= 'Контент', blank=True, null=True)
    image = models.ImageField(upload_to='Img/', default='', verbose_name='Изображение')
    block = models.ForeignKey(Block,default='', verbose_name='Блок', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
    def __unicode__(self):
        return self.block.short_name + ' || ' + self.short_name

class Visitor(models.Model):
    time = models.DateTimeField(auto_now_add = True ,verbose_name='Дата входа')
    remote_adr = models.CharField(max_length=100,default='',verbose_name='IP')
    city = models.CharField(max_length=100,default='',verbose_name='Город')
    region = models.CharField(max_length=100,default='',verbose_name='Область')
    time_zone = models.CharField(max_length=100,default='',verbose_name='Временная зона')
    refer = models.TextField(max_length=2000,default='',verbose_name='Линк')
    browser = models.CharField(max_length=200,default='',verbose_name='Браузер')
    version = models.CharField(max_length=200,default='',verbose_name='Версия браузера')
    device = models.CharField(max_length=200,default='',verbose_name='Устройстово')
    os = models.CharField(max_length=200,default='',verbose_name='ОС')
    source = models.CharField(max_length=200,default='',verbose_name='Источник')


    class Meta:
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'

    def __unicode__(self):
        return self.source + ' || ' + self.browser + '\t||\t' + self.device + '\t||\t' + self.time.strftime("%d.%m.%Y %H:%M:%S")


