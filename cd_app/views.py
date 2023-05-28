from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CsvFileSerializer
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CsvFile
from .calculate_comunitys import leiden
from communityAPI import settings
from rest_framework.response import Response
import os
from .calculate_best_nodes import calculate_best_nodes


class CsvUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = CsvFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file = file_serializer.data.get('file')
            file = str(file)
            file = file.replace("/", "", 1)
            comms, nom_of_communitys = leiden(file)
            svg_path = os.path.join(settings.BASE_DIR, 'images', 'myfile.svg')
            best_nodes, community_with_best_nodes = calculate_best_nodes(file)
            return Response([
  {
    "nodes with most influence :": best_nodes,
    "communitys have best nodes :": community_with_best_nodes,
    "svg_src:": svg_path,
    "number of communitys": nom_of_communitys,
  }], status=201)

        else:
            return Response(file_serializer.errors, status=400)


class CsvDataView(APIView):
    def get(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')
        try:
            csv_file = CsvFile.objects.get(id=file_id)
            file_path = csv_file.file.path
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = [row for row in reader]
            return Response(data, status=200)
        except CsvFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)
