from django.contrib import admin
from db.models import *

class BlockAdmin(admin.ModelAdmin):
    list_display = ['full_name','short_name',]
    ordering = ['full_name']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['block', 'short_name','ord','content']
    list_filter = ['block','short_name']
    ordering = ['block','short_name','ord']

class VisitorAdmin(admin.ModelAdmin):
    list_display = ['time','device','browser','city']
    list_filter = ['browser','city','device']
    ordering = ['-time']

class PictureAdmin(admin.ModelAdmin):
    list_display = ['block','short_name','description']
    list_filter = ['block']
    ordering = ['block','short_name']



admin.site.register(Article,ArticleAdmin)
admin.site.register(Block,BlockAdmin)
admin.site.register(Picture,PictureAdmin)
admin.site.register(Visitor,VisitorAdmin)
