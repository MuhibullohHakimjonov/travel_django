from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth import login, logout
from .forms import *
from django.views.generic import UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def get_client_ip(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_views(obj):
    count = obj.views.count()
    return count


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'travel/index.html', context)


class SearchView(ListView):
    model = Article
    template_name = 'travel/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(title__icontains=word)
        return articles

def category_view(request, pk):
    category = Category.objects.get(pk=pk)
    articles = Article.objects.filter(category=category)
    context = {
        'articles': articles,
        # 'title': {category.title}
    }
    return render(request, 'travel/index.html', context)


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    ip = get_client_ip(request)
    if IpAdress.objects.filter(ip=ip).exists():
        article.views.add(IpAdress.objects.get(ip=ip))
    else:
        IpAdress.objects.create(ip=ip)
        article.views.add(IpAdress.objects.get(ip=ip))
    views = get_views(article)
    context = {
        'article': article,
        'title': f'Статья: {article.title}',
        'comment_form': CommentForm(),
        'comments': Comments.objects.filter(article=article, parent=None),
        'views': views
    }
    return render(request, 'travel/detail.html', context)


def save_comment(request, article_id):
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = Article.objects.get(pk=article_id)
        comment.auth = request.user
        parent_pk = request.POST.get('comment_id')
        if parent_pk:
            comment.parent = Comments.objects.get(pk=parent_pk)
        comment.save()
        return redirect('detail', article_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, auth=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий успешно удален')
        return redirect('detail', pk=comment.article.pk)
    return render(request, 'travel/comment_confirm_delete.html', {"comment": comment})


@login_required()
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, auth=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("detail", pk=comment.article.pk)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'travel/edit_comment.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                try:
                    profile = Profile.objects.get(user=user)
                except:
                    profile = Profile.objects.create(user=user)
                    profile.save()
                return redirect('index')
            else:
                return redirect('index')
        else:
            return redirect('index')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect('index')
        else:
            return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            article.save()
            return redirect('detail', article.pk)
    else:
        form = ArticleForm()

    context = {
        'title': 'Создание статьи',
        'form': form
    }
    return render(request, "travel/article_form.html", context)


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'travel/article_form.html'
    extra_context = {
        "title": 'Изменение статьи'
    }


class ArticleDelete(DeleteView):
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')


def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    articles = Article.objects.filter(author_id=pk)
    context = {
        'profile': profile,
        'articles': articles
    }
    return render(request, 'travel/profile.html', context)


class EditProfile(UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'travel/article_form.html'
    extra_context = {
        'title': 'Изменение профиля'
    }


class EditUser(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'travel/article_form.html'
    extra_context = {
        'title': 'Изменение Профиля'
    }

    def get_success_url(self):
        return self.object.profile.get_absolute_url()
