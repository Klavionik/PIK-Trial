from .serializers import Building


def test_serializer():
    from datetime import datetime
    from django.utils import timezone

    tz = timezone.get_current_timezone()
    date = datetime.strptime('2025-10-10', '%Y-%m-%d')
    date = timezone.make_aware(date, tz, is_dst=None)
    house = Building(address='Мира 14', built=date)