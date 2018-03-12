from .models import Profile
from utils.serializers import DefaultModelSerializer


class ProfileSerializer(DefaultModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'address',
            'date_of_birth',
            'phone_number',
            'umpire_accreditation',
            'created',
            'last_updated',
            'uuid'
        ]

    # What to test on a serializer?
    # Compare serializer.Meta.model to the model we're setting
    # Compare the fields that are available are in the serializer
    # Test the fields are required or not, read_only or not.
