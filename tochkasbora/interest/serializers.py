from rest_framework import serializers

from interest.models import Interest


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'name')
