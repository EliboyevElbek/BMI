from django.db import models
from django.conf import settings
from accounts.models import CustomUser

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Toifa nomi')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

class LessonName(models.Model):
    lesson_name = models.CharField(max_length=50, verbose_name='Kursning nomi')
    lesson_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Toifasi')
    lesson_banner = models.ImageField(upload_to='media/banner/', verbose_name='Banner rasm')
    lesson_price = models.CharField(max_length=7, verbose_name="Kurs narxi", default="Bepul")
    lesson_author_name = models.CharField(max_length=50, verbose_name='Dars muallifi', default='admin')
    lesson_description = models.CharField(max_length=500, verbose_name='Dars haqida umumiy ma\'lumot', default='')

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name_plural = 'LessonNames'
        verbose_name = 'LessonName'

class Lessons(models.Model):
    lesson = models.FileField(upload_to='media/videos/', verbose_name='Darslar')
    lessons_name = models.ForeignKey(LessonName, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.lessons_name}-{self.id}'

    class Meta:
        verbose_name_plural = 'Lessons'
        verbose_name = 'Lessons'

class Stars(models.Model):
    stars = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Baho'
    )
    stars_lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stars_lesson}: {self.from_user} -> {self.stars}'

    class Meta:
        verbose_name_plural = 'Stars'
        verbose_name = 'Stars'
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'stars_lesson'], name='unique_user_lesson_rating')
        ]


class Comments(models.Model):
    comment = models.CharField(max_length=500, verbose_name='Izoh')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_comment = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    datetime_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment[:27]}..."

    class Meta:
        verbose_name_plural = 'Comments'
        verbose_name = 'Comments'

class PaymentUser(models.Model):
    card_nums = models.CharField(max_length=16, verbose_name="Karta raqami")
    card_expiry = models.CharField(max_length=5, verbose_name='Kartani amal qilish muddati')
    payment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_lesson = models.ForeignKey(LessonName, on_delete=models.SET_NULL, null=True,
                                       blank=True)
    paymend_price = models.CharField(max_length=7, verbose_name="To'lov qilingan summa")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_user.phone_number} - {self.card_nums}"








