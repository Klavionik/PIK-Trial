from django.utils import timezone
from rest_framework import serializers

from .models import Building, Job


class RelatedBuildingField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        building_id = self.context['view'].kwargs.get('id')
        queryset = Building.objects.filter(id=building_id)
        return queryset


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'address', 'built']

    def validate_built(self, value):
        now = timezone.now()
        if now > value:
            raise serializers.ValidationError(
                'Дата окончания строительства не должна быть в прошлом')


class JobSerializer(serializers.ModelSerializer):
    building = RelatedBuildingField()

    class Meta:
        model = Job
        fields = ['id', 'bricks_amount', 'execution_time', 'building']

    def validate(self, data):
        now = timezone.now()
        execution_time = data.get('execution_time')
        building = data.get('building')

        if execution_time > building.built:
            raise serializers.ValidationError(
                'Дата задания позже даты окончания строительства')
        if now > execution_time:
            raise serializers.ValidationError(
                'Дата задания не должна быть в прошлом')
        return data
