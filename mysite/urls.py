from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', include('article.urls'))
]