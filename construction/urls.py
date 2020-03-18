from django.urls import path

from .views import BuildingView, JobView, StatsView

urlpatterns = [
    path('building/', BuildingView.as_view()),
    path('building/<int:id>/add_bricks/', JobView.as_view()),
    path('stats/', StatsView.as_view())
]
