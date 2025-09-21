from django.db import models
from django.contrib.auth.models import User

class CropInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crop_inputs")
    features = models.JSONField()  # store list of floats
    soilType = models.CharField(max_length=100, blank=True)
    recommended_crop = models.CharField(max_length=100, blank=True)
    probabilities = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
