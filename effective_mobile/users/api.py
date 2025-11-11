from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from users.models import User, AccessRoleRule
from users.serializers import UserRegisterSerializer, UserLoginSerializer
from users.serializers import UserDetailSerializer, UserUpdateSerializer
from users.serializers import EmptySerializer, RoleUpdateSerializer
from users.jwt import generate_jwt, decode_jwt, get_user_data


@extend_schema(tags=["Authentication"])
class RegisterView(CreateAPIView):
    """API регистрации пользователя"""
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt(user)
            return Response({
                "user": UserDetailSerializer(user).data,
                "token": token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication"])
class LoginView(CreateAPIView):
    """API login пользователя"""
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            user = User.objects.get(email=data['email'], is_active=True)
        except User.DoesNotExist:
            return Response(
                {"error": "Введен неправильный пароль или email"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.check_password(data['password']):
            token = generate_jwt(user)
            response = Response({"token": token, "user": UserDetailSerializer(user).data})
            response.set_cookie(key="user_access_token", value=token, httponly=True)
            return response
        return Response(
            {"error": "Введен неправильный пароль или email"},
            status=status.HTTP_400_BAD_REQUEST
            )
    

@extend_schema(tags=["Authentication"])
class LogoutView(CreateAPIView):
    """API logout пользователя"""
    serializer_class = EmptySerializer
    
    def post(self, request):
        response = Response(
            {"message": "logout выполнен успешно"}, 
            status=status.HTTP_200_OK
        )
        try:
            response.delete_cookie(key="user_access_token")
        except:
            pass
        return response
    

@extend_schema(tags=['Profile'])
class ProfileView(RetrieveAPIView):
    """API просмотра профиля"""
    serializer_class = UserDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        user = get_user_data(request)

        if not user:
            return Response(
                data={"message": "Для просмотра профиля необходимо войти"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
@extend_schema(tags=["Profile"])
class ProfileDeleteView(DestroyAPIView):
    """API удаления профиля пользователя"""
    serializer_class = EmptySerializer

    def destroy(self, request, *args, **kwargs):
        user = get_user_data(request)
        if not user:
            return Response(
                data={"message": "Для удаления профиля необходимо войти"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user.soft_delete()
        response = Response(
            data={"message": "Пользователь успешно удален"},
            status=status.HTTP_200_OK
        )
        try:
            response.delete_cookie(key="user_access_token")
        except:
            pass
        return response


@extend_schema(tags=["Profile"])
class ProfileUpdateView(UpdateAPIView):
    """API обновления ФИО пользователя"""
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        user = get_user_data(request)
        if not user:
            return Response(
                data={"message": "Для удаления профиля необходимо войти"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(UserDetailSerializer(user).data)


@extend_schema(tags=["AccessRules"])
class AccessRoleUpdateView(UpdateAPIView):
    """API обновления прав доступа"""
    serializer_class = RoleUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = AccessRoleRule.objects.all()

    def update(self, request, *args, **kwargs):
        user = get_user_data(request)
        if not user:
            return Response(
                data={"message": "Войдите, чтобы изменить права доступа"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user.role.name != "admin":
            return Response(
                data={"message": "У вас недостаточно прав"},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)