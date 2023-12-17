from rest_framework import serializers

from interest_group.models import InterestGroup


class InterestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestGroup
        fields = (
            'id',
            'name',
            'description',
            'interests',
            'organizer',
            'participants',
            'max_num_participants',
            'is_open',
        )
        extra_kwargs = {
            'participants': {'read_only': True}
        }
