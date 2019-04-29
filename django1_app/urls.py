from django.urls import path
from django1_app import views

# Template URLS
app_name = 'django1_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
]