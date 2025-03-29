from django.contrib import admin
from .models import Lessons, LessonName, Category, Stars, Comments, PaymentUser

# Register your models here.

admin.site.register(Lessons)
admin.site.register(LessonName)
admin.site.register(Category)
admin.site.register(Stars)
admin.site.register(Comments)
admin.site.register(PaymentUser)
