from rest_framework import serializers
from .models import CsvFile


class CsvFileSerializer(serializers.ModelSerializer):
    num_of_best_nodes = serializers.IntegerField(required=True)

    class Meta:
        model = CsvFile
        fields = ('id', 'file', 'num_of_best_nodes')
