from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class IpAdress(models.Model):
    ip = models.CharField(max_length=255)

    def __str__(self):
        return self.ip


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    publish_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    views = models.ManyToManyField(IpAdress, blank=True, verbose_name='Просмотры')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')

    def get_absolute_url(self):  # new
        return reverse('update', args=[str(self.id)])

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'static/images/pic10.jpg'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comments(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    date_time_create = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='answer')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profiles', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.pk})

    def get_profile_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 'https://bootdey.com/img/Content/avatar/avatar7.png'
