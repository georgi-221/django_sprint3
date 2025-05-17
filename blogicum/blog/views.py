from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lt=timezone.now(),
        category__is_published=True
    ).select_related('category')


def index(request):
    return render(
        request,
        'blog/index.html',
        {'post_list': get_published_posts()[:5]}
    )


def post_detail(request, id):
    post = get_object_or_404(get_published_posts(), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, id):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=id
    )
    post_list = get_published_posts().filter(category=category)
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': post_list
        }
    )