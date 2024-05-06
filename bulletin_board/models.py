from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class Bulletin(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    text = RichTextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through = 'BulletinToCategory')


    def __str__(self):
        return f'{self.header} {self.text[:10]} {self.date}'

    def get_absolute_url(self):
        return reverse('bulletin', args=[str(self.pk)])

    def preview(self):
        return self.text[0:123] + '...'


class BulletinToCategory(models.Model):
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Response(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['bulletin', 'author']

    def __str__(self):
        return f'{self.author.user.username} - {self.text[:20]}'

    def get_absolute_url(self):
        return f'/response/{self.id}'

