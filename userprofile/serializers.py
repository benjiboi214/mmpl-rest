from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['address']
    
    # What to test on a serializer?
    # Compare serializer.Meta.model to the model we're setting
    # Compare the fields that are available are in the serializer
    # Test the fields are required or not, read_only or not.