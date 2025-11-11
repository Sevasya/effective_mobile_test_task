from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from django.conf import settings
from users.models import User


JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

def generate_jwt(user):
    payload = {
        "user_id": str(user.id),
        "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(claims=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        return None
    
    user_id = payload.get('user_id')

    try:
        user = User.objects.get(id=user_id, is_active=True)
        return user
    except User.DoesNotExist:
        return None

def get_user_data(request):
    try:
        user = decode_jwt(request.COOKIES['user_access_token'])
        return user
    except:
        return None