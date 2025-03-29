from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StarsAPIView,
    LessonsUpdateAPIView,
    LessonNameUpdateAPIView,
    LessonNameAPIView,
    LessonsListAPIView,
    LessonRetrieveAPIView,
    CategoryViewSet,
    CommentViewSet,
    UserPaymentView, PaymentStoryView,
)
router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('stars/', StarsAPIView.as_view()),
    path('lessons/', LessonsListAPIView.as_view()),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view()),
    path('lessons/<int:pk>/update/', LessonsUpdateAPIView.as_view()),
    path('lesson-names/', LessonNameAPIView.as_view()),
    path('lesson-names/<int:pk>/', LessonNameUpdateAPIView.as_view()),
    path('payment/<int:lesson_id>/', UserPaymentView.as_view()),
    path("payment/story/", PaymentStoryView.as_view())
]
