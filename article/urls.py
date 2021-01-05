from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleView, name='articles'),
    path('detail/<int:article_id>/', views.detail, name='article_detail'),
    path('like', views.LikeView, name='like'),
    path('comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
    path('contact/result/', views.ContactResultView.as_view(), name='contact_result'),   
    #アカウント作成のurl
    path('accounts/signup/', views.signup , name='signup'),
    
]