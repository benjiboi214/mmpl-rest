from .models import Profile, Claim
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


class ClaimSerializer(DefaultModelSerializer):
    class Meta:
        model = Claim
        fields = [
            # System
            'created',
            'last_updated',
            'uuid',
            # Fields
            'id_code',
            'user',
            'profile'
        ]