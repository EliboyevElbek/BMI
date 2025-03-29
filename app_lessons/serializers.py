from rest_framework import serializers
from .models import Comments, Category, Stars, Lessons, LessonName, PaymentUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentsSerializers(serializers.ModelSerializer):
    # from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
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
    class Meta:
        model = Lessons
        fields = ['lessons_name', 'lesson']

class LessonsNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = LessonName
        fields = '__all__'
        depth = 1

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