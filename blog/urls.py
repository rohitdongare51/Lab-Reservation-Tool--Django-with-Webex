from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView,
    PostDeleteView,
    UserPostListView
    )
from testbeds import views as testbeds_views
from chatbot import views as chatbot_views
from . import views
from users import views as users_views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('testbed-home/',testbeds_views.TestbedListView.as_view(template_name='testbeds/testbed-home.html'),name="testbed-home"),
    path('location-detail/<str:parameter>/',testbeds_views.TestbedDetailListView.as_view(template_name='testbeds/location-detail.html'),name="location-detail"),
    path('location-detail/<int:pk>/update/',testbeds_views.TestbedUpdateView.as_view(template_name='testbeds/testbed-detail.html'),name="testbed-detail"),
    path('location-detail/<int:pk>/delete/',testbeds_views.TestbedDeleteView.as_view(template_name='testbeds/testbed-delete.html'),name="testbed-delete"),
    path('testbed_form/',testbeds_views.PostTestbed.as_view(template_name='testbeds/testbed_form.html'),name="testbed_form"),
    path('about/', views.about, name='blog-about'),
    path('chatbot/', chatbot_views.chatbot, name='chatbot'),
    path('getResponse/', chatbot_views.getResponse, name='getResponse'),


    # path('custom_404/', views.custom_404, name='blog-404'),
]

# <app>/<model>_<viewtype>.html