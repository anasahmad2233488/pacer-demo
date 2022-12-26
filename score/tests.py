from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from .models import Score
from django.contrib.auth.models import User
from .views import GetScoreView
import os

class GetScoreTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User(first_name='Test', last_name='User', username='test_user')
        self.user.save()
        self.score = Score(score_a=1, score_b=2, score_c=3, user=self.user)
        self.score.save()
        self.score_pk = self.score.id

    def test_get_correct_score(self):
        factory = APIRequestFactory()
        request = factory.get('score/api/score/{}'.format(self.score_pk), format='json')

        view = GetScoreView.as_view()
        response = view(request, pk=self.score_pk)
        
        a = response.data['score_a']
        b = response.data['score_b']
        c = response.data['score_c']
        total_score = response.data['total_score']

        self.assertEqual(total_score, a*2 + b*4 + c*5)