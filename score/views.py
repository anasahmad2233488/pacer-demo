from rest_framework.generics import views
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Score
from. serializers import GetScoreSerializer

class GetScoreView(views.APIView):


    def get(self, request, *args, **kwargs):
        user_id = int(kwargs['pk'])

        user_query = User.objects.filter(id=user_id)
        if len(user_query) == 0:
            return Response({'message': 'Something wrong.'}, status=404)

        score_query = Score.objects.filter(user_id=user_id)
        if len(score_query) == 0:
            return Response({'message': 'Score is not available.'}, status=404)

        serializer = GetScoreSerializer(score_query[0])
        data = serializer.data
        return Response(data, status=404)

