
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser, IsAuthenticated,
)

from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.views import APIView, Response

from .filter import LessonNameFilter
from .permissions import IsOwnerOfComment, CustomCategoryPermission
from .models import Category, Comments, Stars, Lessons, LessonName, PaymentUser

from .serializers import (
    CategorySerializer,
    CommentsSerializers,
    StarsSerializers,
    LessonsSerializers,
    LessonsNameSerializers, PaymentUserStorySerializer,
)
from rest_framework.generics import get_object_or_404

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomCategoryPermission]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOfComment]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        if lesson_id:
            return Comments.objects.filter(video_comment_id=lesson_id)
        return Comments.objects.all()

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = get_object_or_404(Lessons, id=lesson_id)
        serializer.save(from_user=self.request.user, video_comment=lesson)


class StarsAPIView(ListCreateAPIView):
    queryset = Stars.objects.all()
    serializer_class = StarsSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson_id = self.request.data.get('stars_lesson')
        user = self.request.user

        if Stars.objects.filter(from_user=user, stars_lesson_id=lesson_id).exists():
            raise ValidationError("Siz ushbu darsga allaqachon baho bergansiz.")

        serializer.save(from_user=user)

class LessonsListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializers

class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializers

class LessonsUpdateAPIView(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializers
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class LessonNameAPIView(ListAPIView):
    queryset = LessonName.objects.all()
    serializer_class = LessonsNameSerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = LessonNameFilter
    search_fields = ['lesson_category__category_name']


class LessonNameUpdateAPIView(mixins.UpdateModelMixin,
                              GenericAPIView):
    queryset = LessonName.objects.all()
    serializer_class = LessonsNameSerializers
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserPaymentView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfComment]

    def get(self, request, lesson_id):
        user = request.user
        phone_number = user.phone_number

        lesson = LessonName.objects.get(id=lesson_id)

        data = {
            "phone_number": phone_number,
            "lesson_name": lesson.lesson_name,
            "lesson_price": lesson.lesson_price,
            "card_number": "",
            "card_expiry": ""
        }
        return Response(data)

    # account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    # auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    # client = Client(account_sid, auth_token)
    #
    # media = (
    #     client.messages("SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     .media("MEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     .fetch()
    # )
    #
    # print(media.account_sid)
    # def send_sms(to_phone, message):
    #     account_sid = "YOUR_TWILIO_ACCOUNT_SID"
    #     auth_token = "YOUR_TWILIO_AUTH_TOKEN"
    #     twilio_phone = "YOUR_TWILIO_PHONE_NUMBER"
    #
    #     client = Client(account_sid, auth_token)
    #
    #     try:
    #         message = client.messages.create(
    #             body=message,
    #             from_=twilio_phone,
    #             to=to_phone
    #         )
    #         return {"success": True, "message_sid": message.sid}
    #     except Exception as e:
    #         return {"success": False, "error": str(e)}


    def post(self, request, lesson_id):
        user = request.user
        card_number = request.data.get("card_number")
        card_expiry = request.data.get("card_expiry")
        lesson_price = request.data.get("lesson_price")

        try:
            payment_lesson = LessonName.objects.get(id=lesson_id)
        except LessonName.DoesNotExist:
            return Response({"error": "Dars topilmadi"}, status=404)


        if not card_number or not card_expiry:
            return Response({"error": "Karta raqami va muddati talab qilinadi"}, status=400)

        payment = PaymentUser.objects.create(
            payment_user=user,
            card_nums=card_number,
            card_expiry=card_expiry,
            paymend_price=lesson_price,
            payment_lesson=payment_lesson
        )

        return Response({
            "message": "To‘lov ma’lumotlari saqlandi!",
            "payment_id": payment.id,
            "card_number": payment.card_nums,
            "user": user.username,
            "money": payment.paymend_price,
            "lesson_name": payment.payment_lesson.lesson_name
        }, status=201)


        # sms_response = send_sms(
        #     phone_number,
        #     f"To‘lov muvaffaqiyatli amalga oshirildi! \nKurs: {lesson.lesson_name}, \nKarta: ***{card_number[-4:]}")
        # print(sms_response)

class PaymentStoryView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfComment]

    def get(self, request):
        user = request.user
        payments = PaymentUser.objects.filter(payment_user=user)
        serializer = PaymentUserStorySerializer(payments, many=True)
        return Response(serializer.data)