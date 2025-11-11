from django.urls import path
from users import api


urlpatterns = [
    path("register/", api.RegisterView.as_view(), name="register"),
    path("login/", api.LoginView.as_view(), name="login"),
    path("logout/", api.LogoutView.as_view(), name="logout"),
    path("profile_view/", api.ProfileView.as_view(), name="profile_view"),
    path("profile_delete/", api.ProfileDeleteView.as_view(), name="profile_delete"),
    path("profile_update/", api.ProfileUpdateView.as_view(), name="profile_update"),
    path("access_role_update/<int:id>/", 
         api.AccessRoleUpdateView.as_view(), 
         name="access_role_update"),
]