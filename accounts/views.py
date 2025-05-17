from rest_framework.decorators import api_view
from config.settings import email_send, EMAIL_HOST_USER
from random import randint

from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializers, UserUpdateSerializer

# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = UserSerializers

    def perform_create(self, serializer):
        serializer.save()

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
def send_mail_for_password(request):
    if request.method == 'POST':
        email = request.data['email']
        if CustomUser.objects.filter(email=email).exists():
            code = randint(100000, 999999)
            email_send[email] = code
            send_mail(
                subject="Parolni tiklash uchun kod.",
                message=f"Parol: {code}\n\n",
                from_email=EMAIL_HOST_USER,
                recipient_list=[email]
            )
            return Response({'message': 'Email manzilingizga kod jo\'natildi tekshirishingiz mumkin'}, status=200)
        else:
            return Response({'message': 'Ushbu platformadan ro\'yxatdan o\'tganda kiritgan emailgizni kiriting'}, status=400)
    else:
        return Response({'message': 'Email manzilingizni kiriting'}, status=400)

@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        user_code = request.data['code']
        password1 = request.data['password1']
        password2 = request.data['password2']
        if password2 == password1:
            email, code = list(email_send.items())[0]
            if user_code == code:
                user = CustomUser.objects.get(email=email)
                user.set_password(password1)
                user.save()
                email_send.clear()
                return Response({'message': 'Muvaffaqiyatli o\'zgartirildi'}, status=200)
            else:
                return Response({'message': 'Kodni xato kiritdingiz qayta harakat qiling'}, status=400)
        else:
            return Response({'message': 'Iltimos e\'tiborliroq bo\'ling, parollar bir xil bo\'lishi kerak'}, status=400)



