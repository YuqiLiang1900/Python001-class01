from django.urls import path

from . import views

app_name = 'sentiment'

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.product_view, name='product'),
    path('comments', views.comment_view, name='comment'),
]

