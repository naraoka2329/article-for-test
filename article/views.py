from django.shortcuts import get_object_or_404, render, redirect
from .models import Article, Like, Comment
from django.http import JsonResponse
from .forms import CmtForm, ContactForm
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import json


def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article).order_by('created_at')
    if request.method == "POST":
        print("POST:")
        print("hoge")
        #form = CmtForm(request.POST or None)
        #if form.is_valid():
        texthoge = request.POST.get('text')
        comment = Comment.objects.create(article=article, user=request.user, text=texthoge)
        comment.save()
        
    else:
        print("else:")
        form = CmtForm()
    context = {
        'article': article,
        'comments': comments,
        #'form': form,
    }
    if request.is_ajax():
        print("ajax request.method", request.method)
        print("ajax request.is_ajax", request.is_ajax())
        print("hage")
        html = render_to_string('article/comment.html', context, request=request )
        return JsonResponse({'form': html, })    

    return render(request, 'article/detail.html', context)

def ArticleView(request):
    articles = Article.objects.all()
    liked_list = []
    for article in articles:
        #userが過去にどの記事にいいねしたかをlikedへ格納
        #like_setでarticleに紐づくすべてのいいねを取得し、閲覧しているuserでfilter
        if request.user.is_anonymous == False:
            liked = article.like_set.filter(user=request.user)
            if liked.exists():
                liked_list.append(article.id)

    context = {
        'articles': articles,
        'liked_list': liked_list,
    }

    return render(request, 'article/articles.html', context)

@login_required
def LikeView(request):
    print("ハートが押されたよ")
    #POSTつまり「いいねの押下」で呼ばれないと何もしない
    #最後のif request.is_ajaxで返しているようにAjax通信でなければなにもreturnしない
    if request.method == "POST":
        print(request.body)
        print(request.POST)
        print(json.loads(request.body))
        print('LikeViewのif request.method=="POST"の中')
        #article = get_object_or_404(Article, pk=request.POST.get('article_id'))
        
        article_id = json.loads(request.body)['article_id']
        article = get_object_or_404(Article, pk=article_id)
        user = request.user
        liked = False
        like = Like.objects.filter(article=article, user=user)
        if like.exists():
            print('LikeViewのif like.exists()')
            like.delete()
        else:
            print('LikeViewのif like.exists():else')
            like.create(article=article, user=user)
            liked = True
        
        context = {
            'article_id': article.id,#記事のid
            'liked': liked,#いいねしたのか(True)、いいねを取り消したのか(False)
            'count': article.like_set.count(),#記事のいいね総数
        }
        print(context)
    #if request.is_ajax():
    #    print('LikeViewのif request.is_ajax()の中')
        return JsonResponse(context)
    #else:
    #    print("LikeViewのこれはis_ajax()がfalse")

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('article_detail', article_id=comment.article.id)

class ContactFormView(FormView):
    template_name = 'contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_result')

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)

class ContactResultView(TemplateView):
    template_name = 'contact/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました"
        return context

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #dict型[]
            input_username = form.cleaned_data["username"]
            input_password = form.cleaned_data["password1"]
            #ユーザを認証する
            new_user = authenticate(username=input_username, password=input_password)
            if new_user is not None:
                #ユーザをログイン状態にする
                login(request, new_user)
                return redirect('articles')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})