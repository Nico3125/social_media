"""Mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('Posts.urls')),
    path('inregistrare/', views.inregistrare, name='posts_inregistrare'),
    path('login/', views.login, name='posts-login'),
    path('profile/', views.my_profile, name='profile'),
    # path('', include('feed.urls')),
    path('posts/users_list', views.users_list, name='users_list'),
    path('posts/user_event', views.UserEventListView.as_view(template_name='user_event.html'), name='user_event'),
    path('posts/<slug>/', views.profile_view, name='profile_view'),
    path('posts/friend_list/', views.friend_list, name='friend_list'),
    path('friend-request/send/<int:id>/', views.send_friend_request, name='send_friend_request'),
    path('friend-request/cancel/<int:id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('friend-request/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/delete/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
    # path('friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search_users/', views.search_users, name='search_users'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
