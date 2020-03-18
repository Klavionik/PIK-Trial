from rest_framework import generics
from rest_framework import mixins

from .models import Building, Job
from .serializers import BuildingSerializer, JobSerializer


class BuildingView(mixins.ListModelMixin,
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


class StatsView(generics.GenericAPIView):
    pass
