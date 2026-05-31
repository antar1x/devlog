from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import UserRegistrationView, CustomLoginView, HomeView, ProfileView, PublicProfileView, \
    MyProfileView, MyProfileInfoView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('profiles/search/', ProfileView.as_view(), name='profiles'),
    path('u/<str:username>/', PublicProfileView.as_view(), name='public_profile'),
    path('profile/settings/', MyProfileView.as_view(), name='profile_settings'),
    path('profile/', MyProfileInfoView.as_view(), name='profile_info'),
]
