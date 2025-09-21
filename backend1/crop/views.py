from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
import json ,joblib ,os
from django.conf import settings
from crop.serializers import CropInputSerializer,LoginSerializer,RegisterSerializer
from .ml_utils import predict_crop
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated


import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors,
            }, status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()  # Save user
        

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            'status': True,
            'message': 'User registered successfully',
            'data': serializer.data,
            'tokens': tokens
        }, status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data)
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                
                user = authenticate(username=username, password=password)
                if user is None:
                    return Response(
    {'status': False, 'message': 'Invalid username or password', 'data': {}},
    status=status.HTTP_401_UNAUTHORIZED
)

                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': True,
                    'message': 'Login successful',
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            
            return Response(
    {'status': False, 'message': 'Invalid input', 'data': serializer.errors},
    status=status.HTTP_400_BAD_REQUEST
)

       
        except Exception as e:
            print(e)
            return Response({'status': 500, 'message': 'Server error', 'data': {}})
  
                
    
    

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Load your Gemini API key from environment variable
genai.configure(api_key=os.getenv("AIzaSyASzOj0vx6oyZdOXZ0YBpooIU1VotYcOnY"))
# @csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gemini_recommendations(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            ph = body.get("ph")
            moisture = body.get("moisture")
            texture = body.get("texture")
            crop = body.get("crop")

            prompt = f"""
            You are an expert agronomist. Based on this soil analysis:
            - pH level: {ph}
            - Moisture: {moisture}
            - Soil texture: {texture}
            - Recommended crop: {crop}

            Give me 4 practical, actionable farming recommendations to optimize crop yield.
            Write them as short bullet points.
            """

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            # Split response into bullet points
            recs = [r.strip("-• ") for r in response.text.split("\n") if r.strip()]

            return JsonResponse({"recommendations": recs})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def input(request):
    serializer = CropInputSerializer(data=request.data)

    if serializer.is_valid():
        best_crop, probabilities = predict_crop(serializer.validated_data)
        print("****************88",best_crop)
        print("****************88",probabilities)
        crop_input = serializer.save(
        user=request.user,
        recommended_crop=best_crop,
        probabilities=probabilities
    )
        return Response(
            {"recommended_crop": best_crop, "probabilities": probabilities},
            status=status.HTTP_200_OK
        )

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
