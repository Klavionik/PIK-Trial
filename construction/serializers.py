from django.utils import timezone
from rest_framework import serializers

from .models import Building, Job


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'address', 'built']

    def validate(self, data):
        now = timezone.now().year
        if now > data.get('built'):
            raise serializers.ValidationError(
                'Год окончания строительства меньше текущего года')
        return data


class RelatedBuildingField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        building_id = self.context['view'].kwargs.get('id')
        queryset = Building.objects.filter(id=building_id)
        return queryset


class JobSerializer(serializers.ModelSerializer):
    building = RelatedBuildingField()

    class Meta:
        model = Job
        fields = ['id', 'bricks_amount', 'execution_time', 'building']

    def validate(self, data):
        now = timezone.now()
        execution_time = data.get('execution_time')
        building = data.get('building')

        if execution_time.year > building.built:
            raise serializers.ValidationError(
                'Год задания позже года окончания строительства')
        if now > execution_time:
            raise serializers.ValidationError(
                'Время выполнения задания раньше текущего времени')

        bricks_amount = data.get('bricks_amount')
        if bricks_amount < 1:
            raise serializers.ValidationError(
                'Количество кирпичей меньше 1'
            )
        return data
