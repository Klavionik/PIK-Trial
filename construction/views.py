from django.db.models import Sum
from django.shortcuts import redirect
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Building, Job
from .serializers import BuildingSerializer, JobSerializer


class BuildingView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class JobView(mixins.ListModelMixin,
              mixins.CreateModelMixin,
              generics.GenericAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(building__id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET'])
def stats_view(request):
    buildings = Building.objects.values('id', 'address', 'built').\
        order_by('id').\
        annotate(bricks_total=Sum('jobs__bricks_amount'))

    buildings_stat = {'buildings': {}}

    for building in buildings:
        built = building['built']
        year = buildings_stat['buildings'].setdefault(built, [])
        year.append(
            {
                'address': building['address'],
                'bricks_total': building['bricks_total']
            }
        )

    return Response({'stats': buildings_stat})


def home_view(request):
    return redirect('stats')
