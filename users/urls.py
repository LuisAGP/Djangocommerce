from django.urls import path
from .views import login_view, register_view, logout_view, ProfileView, validate_email

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('validate/<str:id>', validate_email, name="validate_email")
]