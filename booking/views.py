from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import uuid
from core.models import TourPackage, Attraction, Order

def generate_order_no():
    """生成唯一订单号"""
    return timezone.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex[:8])

@login_required
def create_order(request, package_id):
    """创建订单"""
    package = get_object_or_404(TourPackage, id=package_id, is_active=True)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        travel_date = request.POST.get('travel_date')
        contact_name = request.POST.get('contact_name')
        contact_phone = request.POST.get('contact_phone')
        remark = request.POST.get('remark', '')
        
        total_amount = package.price * quantity
        order_no = generate_order_no()
        
        order = Order.objects.create(
            order_no=order_no,
            user=request.user,
            tour_package=package,
            quantity=quantity,
            total_amount=total_amount,
            travel_date=travel_date,
            contact_name=contact_name,
            contact_phone=contact_phone,
            remark=remark,
            status='pending'
        )
        
        messages.success(request, '订单创建成功，请尽快完成支付！')
        return redirect('booking:order_detail', order_no=order_no)
    
    context = {
        'package': package,
        'today': timezone.now().date(),
    }
    return render(request, 'booking/create_order.html', context)

@login_required
def create_ticket_order(request, attraction_id):
    attraction = get_object_or_404(Attraction, id=attraction_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        travel_date = request.POST.get('travel_date')
        contact_name = request.POST.get('contact_name')
        contact_phone = request.POST.get('contact_phone')
        remark = request.POST.get('remark', '')
        
        total_amount = attraction.ticket_price * quantity
        order_no = generate_order_no()
        
        order = Order.objects.create(
            order_no=order_no,
            user=request.user,
            product_type='ticket',
            attraction=attraction,
            quantity=quantity,
            total_amount=total_amount,
            travel_date=travel_date,
            contact_name=contact_name,
            contact_phone=contact_phone,
            remark=remark,
            status='pending'
        )
        messages.success(request, '门票订单创建成功，请尽快支付！')
        return redirect('booking:order_detail', order_no=order_no)
    
    context = {
        'attraction': attraction,
        'today': timezone.now().date(),
    }
    return render(request, 'booking/create_ticket_order.html', context)

@login_required
def order_detail(request, order_no):
    """订单详情"""
    order = get_object_or_404(Order, order_no=order_no, user=request.user)
    context = {'order': order}
    return render(request, 'booking/order_detail.html', context)

@login_required
def my_orders(request):
    """我的订单列表"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'booking/my_orders.html', context)

@login_required
def pay_order(request, order_no):
    """支付订单（模拟支付）"""
    order = get_object_or_404(Order, order_no=order_no, user=request.user)
    
    if request.method == 'POST':
        # 模拟支付成功
        order.status = 'paid'
        order.save()
        messages.success(request, '支付成功！')
        return redirect('booking:order_detail', order_no=order_no)
    
    context = {'order': order}
    return render(request, 'booking/pay.html', context)
