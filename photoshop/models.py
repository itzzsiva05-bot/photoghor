from django.db import models


class Register(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField()

    def __str__(self):
        return self.title

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    
    def __str__(self):
        return f"Gallery {self.id}"