from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json ,joblib ,os
from django.conf import settings
from crop.serializers import CropInputSerializer
from .ml_utils import predict_crop
from rest_framework import viewsets,status



@api_view(['POST'])
def input(request):
    serializer = CropInputSerializer(data=request.data)

    if serializer.is_valid():
        crop = predict_crop(serializer.validated_data)
        return Response({"recommended_crop": crop}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def input(request):
#     if request.method== 'POST':
#         data = json.loads(request.body)
#         print(data)
#         serializer = CropInputSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
