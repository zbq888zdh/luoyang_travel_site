from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('create/<int:package_id>/', views.create_order, name='create_order'),
    path('order/<str:order_no>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('pay/<str:order_no>/', views.pay_order, name='pay_order'),
    path('ticket/<int:attraction_id>/', views.create_ticket_order, name='create_ticket_order'),
]