from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),                          # 首页
    path('attractions/', views.attraction_list, name='attraction_list'),  # 景点列表
    path('attraction/<int:id>/', views.attraction_detail, name='attraction_detail'),  # 景点详情
    path('search/', views.search, name='search'),               # 搜索功能
    path('map/', views.map_view, name='map'),                   # 地图页面
    path('packages/', views.package_list, name='package_list'), # 旅游套餐列表
]