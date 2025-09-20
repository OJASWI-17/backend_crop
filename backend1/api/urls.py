from crop.views import input,gemini_recommendations,LoginAPI
from django.urls import path,include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'input', input,basename='input')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#     (class) TokenObtainPairView
# Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.
#   (class) TokenRefreshView
# Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

urlpatterns = [
    path('input/', input),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginAPI.as_view()),
    # path('register/', RegisterAPI.as_view()),
    path("gemini/recommendations/", gemini_recommendations),
    # path('login/', login),
    # path('persons/', PersonAPI.as_view()),
    path('',include(router.urls)),
]