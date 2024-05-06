from django.contrib import admin
from .models import Profile, Bulletin, Category, BulletinToCategory, Response


# Register your models here.
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Bulletin)
admin.site.register(BulletinToCategory)
admin.site.register(Response)