from rest_framework import serializers
from apiapp.models import JSONRecieved

Class JSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = JSONRecieved
        fields = ('key','text','riskIndex','color','shape')