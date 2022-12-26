from django.urls import path
from .views import GetScoreView

urlpatterns = [
    path('api/score/<pk>', GetScoreView.as_view(), name='get-score')
]