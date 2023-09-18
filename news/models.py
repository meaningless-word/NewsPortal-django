from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой публикации автора
        post_rating = 0
        if self.post_set.exists():
            post_rating_sum = self.post_set.aggregate(pr=Sum('rating'))
            post_rating += post_rating_sum.get('pr')

        # суммарный рейтинг комментариев автора
        comment_rating = 0
        if self.user.comment_set.exists():
            comment_rating_sum = self.user.comment_set.aggregate(cr=Sum('rating'))
            comment_rating += comment_rating_sum.get('cr')

        # суммарный рейтинг комментариев к публикациям автора
        # считаю, не совсем корректно его учитывать, поскольку задизлайканный очерняющий комментарий под хорошей статьёй снижает рейтинг автора публикации
        # хотя, должен отражаться только на рейтинге комментатора
        post_comment_rating = 0
        if Comment.objects.filter(post__author=self).exists():
            post_comment_rating_sum = Comment.objects.filter(post__author=self).aggregate(cpr=Sum('rating'))
            post_comment_rating += post_comment_rating_sum.get('cpr')

        self.rating = post_rating * 3 + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return f'{self.user.username} [{self.rating}]'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:40]} ... [{str(self.rating)}]'

    def __str__(self):
        return f'{self.title} {self.preview()}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} : {self.category.name}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[:20]}... [{self.rating}]'
