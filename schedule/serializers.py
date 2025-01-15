from rest_framework import serializers
from .models import Schedule
from core.serializers import UserSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Schedule
        fields = '__all__'
        depth = 1

class SchedulePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

