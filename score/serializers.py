from rest_framework import serializers
from .models import Score

class GetScoreSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField('get_total_score')    

    class Meta:
        model = Score
        fields = [
            'user', 
            'score_a', 
            'score_b', 
            'score_c',
            'total_score'
            ]
    
    def get_total_score(self, score):
        a = score.score_a
        b = score.score_b
        c = score.score_c
        return a*2 + b*4 + c*5