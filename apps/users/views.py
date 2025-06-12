from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SignupSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



User = get_user_model()

# 회원가입
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입을 성공했습니다"}, status=201)
        return Response(serializer.errors, status=400)

# 로그인
class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            email=request.data.get("email"),
            password=request.data.get("password")
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        return Response({"detail": "로그인에 실패하였습니다"}, status=401)

#로그아웃
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh = RefreshToken(request.data.get("refresh"))
            refresh.blacklist()
            return Response({"message": "로그아웃"}, status=205)
        except Exception:
            return Response({"message": "잘못된 토큰"}, status=400)



@csrf_exempt  # CSRF 우회 (POST 요청 위해)
def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(email="admin@example.com").exists():
        User.objects.create_superuser(email="admin@example.com", password="admin1234")
        return JsonResponse({"status": "admin created"})
    return JsonResponse({"status": "already exists"})