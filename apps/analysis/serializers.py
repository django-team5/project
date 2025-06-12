from rest_framework import serializers
from .models import Analysis

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'
        read_only_fields = ['user', 'summary', 'result_image_url', 'created_at']
