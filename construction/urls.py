from django.urls import path

from .views import BuildingView, JobView, stats_view

urlpatterns = [
    path('building/', BuildingView.as_view(), name='building'),
    path('building/<int:id>/add_bricks/', JobView.as_view(), name='add_bricks'),
    path('stats/', stats_view, name='stats')
]
