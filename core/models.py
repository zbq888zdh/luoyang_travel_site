from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import requests

class Category(models.Model):
    """景点分类（如：龙门石窟、白马寺、洛阳博物馆等）"""
    name = models.CharField('分类名称', max_length=50)
    icon = models.CharField('图标', max_length=50, blank=True, help_text='Font Awesome图标类名')
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        verbose_name = '景点分类'
        verbose_name_plural = '景点分类'
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.name

class Attraction(models.Model):
    """景点信息"""
    name = models.CharField('景点名称', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='所属分类')
    description = models.TextField('景点介绍')
    address = models.CharField('详细地址', max_length=200)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, null=True, blank=True)
    ticket_price = models.DecimalField('门票价格', max_digits=10, decimal_places=2, default=0)
    opening_hours = models.CharField('开放时间', max_length=100, default='09:00-17:00')
    phone = models.CharField('咨询电话', max_length=20, blank=True)
    image = models.ImageField('景点图片', upload_to='attractions/', blank=True, null=True)
    view_count = models.IntegerField('浏览次数', default=0)
    is_recommended = models.BooleanField('是否推荐', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '景点'
        verbose_name_plural = '景点'
        ordering = ['-is_recommended', 'id']
    
    def __str__(self):
        return self.name

class TourPackage(models.Model):
    """旅游线路/套餐"""
    TYPE_CHOICES = [
        ('day_trip', '一日游'),
        ('multi_day', '多日游'),
        ('theme', '主题游'),
    ]
    
    name = models.CharField('套餐名称', max_length=100)
    type = models.CharField('套餐类型', max_length=20, choices=TYPE_CHOICES)
    attractions = models.ManyToManyField(Attraction, verbose_name='包含景点')
    description = models.TextField('行程介绍')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    duration_days = models.IntegerField('行程天数', default=1)
    image = models.ImageField('套餐图片', upload_to='packages/', blank=True, null=True)
    is_active = models.BooleanField('是否上架', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '旅游套餐'
        verbose_name_plural = '旅游套餐'
    
    def __str__(self):
        return self.name

class Order(models.Model):
    """订单"""
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    ]
    PRODUCT_TYPE_CHOICES = [
        ('package', '旅游套餐'),
        ('ticket', '景点门票'),
    ]
    order_no = models.CharField('订单号', max_length=32, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    product_type = models.CharField('产品类型', max_length=20, choices=PRODUCT_TYPE_CHOICES, default='package')
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, null=True, blank=True, verbose_name='旅游套餐')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, null=True, blank=True, verbose_name='景点')
    quantity = models.IntegerField('预订数量', default=1)
    total_amount = models.DecimalField('总金额', max_digits=10, decimal_places=2)
    travel_date = models.DateField('出行日期')
    contact_name = models.CharField('联系人姓名', max_length=50)
    contact_phone = models.CharField('联系电话', max_length=20)
    status = models.CharField('订单状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    remark = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.order_no} - {self.user.username}'

class Review(models.Model):
    """用户评价"""
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, verbose_name='景点')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    rating = models.IntegerField('评分', choices=[(i, i) for i in range(1, 6)])
    content = models.TextField('评价内容')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '评价'
        verbose_name_plural = '评价'
    
    def __str__(self):
        return f'{self.user.username} - {self.attraction.name}'
    
def get_real_nearby_pois(self, types='050000|060000', radius=1000):
        """调用高德API获取周边POI"""
        url = 'https://restapi.amap.com/v3/place/around'
        params = {
            'key': '1bbf63742d2732650f31cf30e0266ed3',
            'location': f'{self.longitude},{self.latitude}',
            'radius': radius,
            'types': types,  # 050000=餐饮, 060000=购物
            'output': 'JSON',
            'page_size': 10
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            if data.get('status') == '1':
                return [{'name': poi['name'], 'lat': poi['location'].split(',')[1], 
                         'lng': poi['location'].split(',')[0], 'address': poi['address'], 
                         'type': poi['type']} for poi in data.get('pois', [])]
        except Exception as e:
            print(f"高德API调用失败: {e}")
        return []

def get_real_nearby_pois(self):
        """获取周边POI（暂时返回空列表，避免报错）"""
        # 如果你以后想接入高德API，可以在这里实现
        # 目前先返回空列表，让地图可以正常显示
        return []