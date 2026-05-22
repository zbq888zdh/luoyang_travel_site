from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Attraction, TourPackage, Review
from .forms import ReviewForm

def home(request):
    """首页视图"""
    # 获取推荐景点
    recommended_attractions = Attraction.objects.filter(is_recommended=True)[:6]
    # 获取热门景点（按浏览次数排序）
    popular_attractions = Attraction.objects.order_by('-view_count')[:6]
    # 获取旅游套餐
    tour_packages = TourPackage.objects.filter(is_active=True)[:3]
    
    context = {
        'recommended_attractions': recommended_attractions,
        'popular_attractions': popular_attractions,
        'tour_packages': tour_packages,
    }
    return render(request, 'core/home.html', context)

def attraction_list(request):
    """景点列表视图"""
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword')
    
    attractions = Attraction.objects.all()
    
    if category_id:
        attractions = attractions.filter(category_id=category_id)
    if keyword:
        attractions = attractions.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'attractions': attractions,
        'categories': categories,
        'current_category': category_id,
    }
    return render(request, 'core/attraction_list.html', context)

def attraction_detail(request, id):
    attraction = get_object_or_404(Attraction, id=id)
    # 增加浏览次数
    attraction.view_count += 1
    attraction.save()

    # 获取已有评论
    reviews = Review.objects.filter(attraction=attraction).order_by('-created_at')

    # 处理评论提交
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.attraction = attraction
            new_review.user = request.user
            new_review.save()
            messages.success(request, '评论发布成功！')
            return redirect('core:attraction_detail', id=attraction.id)
    else:
        form = ReviewForm()

    context = {
        'attraction': attraction,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'core/attraction_detail.html', context)

def search(request):
    """搜索功能视图"""
    keyword = request.GET.get('q', '')
    results = []
    if keyword:
        # 搜索景点
        results = Attraction.objects.filter(
            Q(name__icontains=keyword) | 
            Q(description__icontains=keyword) |
            Q(address__icontains=keyword)
        )
    context = {
        'keyword': keyword,
        'results': results,
    }
    return render(request, 'core/search.html', context)

def package_list(request):
    """旅游套餐列表"""
    packages = TourPackage.objects.filter(is_active=True)
    context = {'packages': packages}
    return render(request, 'core/package_list.html', context)

def map_view(request):
    attractions = Attraction.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    # 暂时不加载周边POI，避免报错。如果需要示例数据，可以取消注释下面的代码
    # for attraction in attractions:
    #     attraction.nearby_pois = []   # 或者添加示例POI
    return render(request, 'core/map.html', {'attractions': attractions})
