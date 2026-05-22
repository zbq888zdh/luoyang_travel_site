from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} 星') for i in range(1, 6)]),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': '分享您的游览体验...'}),
        }
        labels = {
            'rating': '评分',
            'content': '评论内容',
        }