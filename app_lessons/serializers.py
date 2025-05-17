from rest_framework import serializers
from .models import Comments, Category, Stars, Lessons, LessonName, PaymentUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentsSerializers(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'comment', 'video_comment', 'datetime_comment', 'from_user']
        read_only_fields = ['datetime_comment', 'from_user']

    def get_from_user(self, obj):
        return {"id": obj.from_user.id, "name": obj.from_user.username}

class StarsSerializers(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    class Meta:
        model = Stars
        fields = ['stars', 'stars_lesson', 'from_user']
        read_only_fields = ['from_user']

    def get_from_user(self, obj):
        return {"id": obj.from_user.id, "name": obj.from_user.username}

class LessonsSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    class Meta:
        model = Lessons
        fields = '__all__'
        depth = 1

    def get_title(self, obj):
        lesson_name = obj.lesson.name
        title = lesson_name.split('/')[-1]
        title = title.replace('_', ' ')
        title = title.split(' ')[1:]
        title[-1]= title[-1].split('.')[0]
        if title[-1].islower() and title[-1].isalpha():
            title = ' '.join(title[:])
        else:
            title = ' '.join(title[:-1])
        return title

import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class LessonsNameSerializers(serializers.ModelSerializer):
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = LessonName
        fields = '__all__'
        depth = 1

    def get_formatted_price(self, obj):
        price = obj.lesson_price
        if price:
            try:
                price = int(price)
                return locale.format_string("%d", price, grouping=True)
            except ValueError:
                return None
        return None


class PaymentUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='payment_user.phone_number', read_only=True)

    class Meta:
        model = PaymentUser
        fields = ['id', 'card_nums', 'card_expiry', 'phone_number']
        extra_kwargs = {'payment_user': {'read_only': True}}

class PaymentUserStorySerializer(serializers.ModelSerializer):
    lesson_name = serializers.CharField(source='payment_lesson.lesson_name', read_only=True)
    lesson_price = serializers.CharField(source='payment_lesson.lesson_price', read_only=True)
    class Meta:
        model = PaymentUser
        fields = ['id', 'lesson_price', 'created_at', 'lesson_name']