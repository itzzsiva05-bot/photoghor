from django.db import models
from django.contrib.auth.models import User


class Register(models.Model):
    username = models.CharField(max_length=100)
    email    = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photo(models.Model):
    category    = models.ForeignKey(
                    Category,
                    on_delete=models.SET_NULL,
                    null=True, blank=True
                  )
    title       = models.CharField(max_length=100)
    image       = models.ImageField(upload_to='photos/')
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def likes_count(self):
        return self.photo_likes.count()

    def __str__(self):
        return self.title


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return f"Gallery {self.id}"


class PhotoLike(models.Model):
    user       = models.ForeignKey(User,  on_delete=models.CASCADE,
                                   related_name='user_likes')
    photo      = models.ForeignKey(Photo, on_delete=models.CASCADE,
                                   related_name='photo_likes')
    liked_date = models.DateField()

    class Meta:
        unique_together = ('user', 'photo', 'liked_date')
        ordering        = ['-liked_date']

    def __str__(self):
        return f"User {self.user_id} liked Photo {self.photo_id} on {self.liked_date}"