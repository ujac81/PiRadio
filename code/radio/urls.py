from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='radio-index'),
#    path('ajax/cmd/', views.cmd_ajax, name='cmd_ajax'),
]
