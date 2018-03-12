from .models import Profile
from utils.serializers import DefaultModelSerializer


class ProfileSerializer(DefaultModelSerializer):
    class Meta:
        model = Profile
        fields = [
            # System
            'created',
            'last_updated',
            'uuid',
            # Fields
            'name',
            'address',
            'phone_number',
            'date_of_birth',
            'umpire_accreditation',
        ]
