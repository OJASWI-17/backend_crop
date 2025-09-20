from django.shortcuts import render
from rest_framework.decorators import api_view,APIView
from rest_framework.response import Response
import json ,joblib ,os
from django.conf import settings
from crop.serializers import CropInputSerializer,LoginSerializer
from .ml_utils import predict_crop
from rest_framework import viewsets,status


import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                
                user = authenticate(username=email, password=password)

                if user is not None:
                    return Response({'status':400,'message':'invalid password','data':{}})
                
                
                refresh = RefreshToken.for_user(user)

                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }   
                
            return Response({'status':400,'message':'something went wrong ','data':serializer.errors})    
            
       
             
        except Exception as e:      
            print(e)
                
                
    
    

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Load your Gemini API key from environment variable
genai.configure(api_key=os.getenv("AIzaSyASzOj0vx6oyZdOXZ0YBpooIU1VotYcOnY"))

@csrf_exempt
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
def input(request):
    serializer = CropInputSerializer(data=request.data)

    if serializer.is_valid():
        best_crop, probabilities = predict_crop(serializer.validated_data)
        print("****************88",best_crop)
        print("****************88",probabilities)
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
