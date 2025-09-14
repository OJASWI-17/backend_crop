from crop.views import input
from django.urls import path,include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'input', input,basename='input')


urlpatterns = [
    path('input/', input),
    # path('login/', login),
    # path('persons/', PersonAPI.as_view()),
    path('',include(router.urls)),
]