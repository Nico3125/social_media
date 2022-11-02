from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import EventUpdateView, EventListView


urlpatterns = [
    path('', views.home, name='posts_acasa'),
    path('Posts', views.index),
    path('about', views.about, name='posts_despre'),
    path('inregistrare/', views.inregistrare, name='posts_inregistrare'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='posts-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='posts-logout'),
    path('password_reset_file/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_file.html'),
         name='password-reset-file'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password)reset_confirm.html'),
         name='password-reset-confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html.html'),
         name='password-reset-done'),

    path('profile/', views.my_profile, name='users-profile'),
    path('', EventListView.as_view(), name='home'),
    path('create_event/', views.create_event, name='create-event'),
    # path('event/<int:pk>/', views.event_detail, name='post-detail'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event-delete'),
    path('search_events/', views.search_events, name='search-events'),
]
