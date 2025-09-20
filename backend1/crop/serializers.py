# from rest_framework import serializers

# class CropInputSerializer(serializers.Serializer):
#     N = serializers.FloatField()
#     P = serializers.FloatField()
#     K = serializers.FloatField()
#     temperature = serializers.FloatField()
#     humidity = serializers.FloatField()
#     ph = serializers.FloatField()
#     rainfall = serializers.FloatField()

from rest_framework import serializers

class CropInputSerializer(serializers.Serializer):
    features = serializers.ListField(
        child=serializers.FloatField(),
        min_length=7,
        max_length=7
    )
    soilType = serializers.CharField(allow_blank=True, required=False)
    
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=6)    
