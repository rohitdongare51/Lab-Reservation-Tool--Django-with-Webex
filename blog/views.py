from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
def home(request):
	context = {
				'posts': Post.objects.all()
				}
	return render(request, 'blog/home.html', context)

@login_required
def about(request):
	return render(request, 'blog/about.html', {'title': 'About Blog'})

def test(request):
	return render(request, 'blog/add_testbed.html', {'title': 'Test Blog'})

def custom_404(request):
	return render(request, 'blog/404.html', {'title': 'Page Not Found'})

@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # paginate_by = 3

    # def get_queryset(self):
    #     # obj = get_object_or_404(Post)
    #     # print(self.request.GET.get('submitted_button'))
    #     blogs = []
    #     if self.request.GET.get('submitted_button'):
    #         searched_blog = self.request.GET.get('search_blog','')
    #         return Post.objects.filter(Q(title__icontains=searched_blog) | Q(content__icontains=searched_blog)).order_by('-date_posted')
    #     return Post.objects.all().order_by('-date_posted')

    def get_context_data(self):
        searched_blog = self.request.GET.get('search_blog','')

        post_obj = Post.objects.all().order_by('-date_posted')
        if searched_blog:
            post_obj = Post.objects.filter(Q(title__icontains=searched_blog) | Q(content__icontains=searched_blog)).order_by('-date_posted')
        paginator = Paginator(post_obj, per_page=3)
        page_number = self.request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        context = {'posts': paginator.page(int(page_number)),"is_paginated":True, 'page_obj': page_obj,'searched_blog': searched_blog}
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False