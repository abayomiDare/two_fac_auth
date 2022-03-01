from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', user),
    path('users/<int:user_id>/', get_userid),
    path('hello/', base_view, name='hello'),
]
