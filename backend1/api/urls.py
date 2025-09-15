from crop.views import input,gemini_recommendations,LoginAPI,RegisterAPI
from django.urls import path,include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'input', input,basename='input')


urlpatterns = [
    path('input/', input),
    path('login/', LoginAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path("gemini/recommendations/", gemini_recommendations),
    # path('login/', login),
    # path('persons/', PersonAPI.as_view()),
    path('',include(router.urls)),
]