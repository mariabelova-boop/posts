from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

#Класс, потом методы

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE) #cвязь «один к одному» с встроенной моделью пользователей User
    ratingAuthor = models.SmallIntegerField(default=0) #рейтинг автора О изначально

    def update_rating(self):
        postRat = self.post_set.agregate(postRating=Sum('rating')) #Складывает все значения поля "Рейтинг" у этого автора. Agrigate = складывание
        pRat = 0
        pRat += postRat.get('PostRating')  #Выводит значение

        commentRat = self.authorUser.comment_set.agregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('PostRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True) #Категории новостей/статей

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE) #связь «один ко многим» с моделью Author

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISE = (
        (NEWS, "Новость"),
        (ARTICLE, "Статья")
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOISE, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory') #связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    heabin = models.CharField(max_length=128)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124]+'. . .'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categotyThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
