from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from app import views as vw

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^visitor/$', views.catch_visitor),
    url(r'^admin/', admin.site.urls),
    url(r'^recall/(-*\d+)/(-*\d+)$', views.recall_base),
    url(r'^subscription/$', views.subscription),
    url(r'^submit/(-*\d+)$', views.submit),
    url(r'^payment-form/(-*\d+)$', views.order_page),
    url(r'^kassa/payment-aviso/', vw.aviso),
    url(r'^kassa/order-check/', vw.check),
    url(r'^kassa/success/', views.success),
    url(r'^kassa/fail/', views.fail),
]\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
