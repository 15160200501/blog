from django.urls import path        #从django.urls导入了path函数
from . import views     #当前目录下导入了views模块

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>', views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>', views.tag, name='tag'),
]
