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
from django.contrib.auth.models import User
from .models import CropInput


# class CropInputSerializer(serializers.Serializer): # not connected to database
#     features = serializers.ListField(
#         child=serializers.FloatField(),
#         min_length=7,
#         max_length=7
#     )
#     soilType = serializers.CharField(allow_blank=True, required=False)
class CropInputSerializer(serializers.ModelSerializer):#  connected to database
    
    class Meta:
        model = CropInput
        fields = ['features', 'soilType']  # input only
    
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # password won't be exposed

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # use explicit fields, not '__all__'

    def validate(self, data):
        errors = {}
        username = data.get('username')
        email = data.get('email')

        if username and User.objects.filter(username=username).exists():
            errors['username'] = ['Username already exists']
        if email and User.objects.filter(email=email).exists():
            errors['email'] = ['Email already exists']

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        # Create user and hash password correctly
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password  = serializers.CharField()    
