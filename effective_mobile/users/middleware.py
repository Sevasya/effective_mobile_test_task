from django.utils.deprecation import MiddlewareMixin
from users.models import User
from users.jwt import decode_jwt

class JWTAuthMiddleware(MiddlewareMixin):
    """Middleware определения пользователя"""
    def process_request(self, request):
        request.user = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_jwt(token)
            if payload:
                try:
                    request.user = User.objects.get(id=payload["user_id"], is_active=True)
                except User.DoesNotExist:
                    pass
