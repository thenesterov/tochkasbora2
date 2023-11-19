from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    # organizer = serializers.HiddenField(default=)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'is_open',
            'max_num_participants',
            'datetime_event',
            'organizer_id',
            'rate',
            'address',
            'interests',
            'participants'
        )
        extra_kwargs = {
            # 'organizer_id': {'read_only': True},
            'rate': {'read_only': True},
            'participants': {'read_only': True}
        }

    # def create(self, validated_data): ...
    # def update(self, instance, validated_data): ...
