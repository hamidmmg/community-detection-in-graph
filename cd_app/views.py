from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CsvFileSerializer
import csv
from rest_framework.views import APIView
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
            num_of_best_nodes = file_serializer.data.get('num_of_best_nodes')
            file = str(file)
            file = file.replace("/", "", 1)
            community_svg_path = os.path.join(settings.BASE_DIR, 'images', 'myfile.svg')
            original_svg_path = os.path.join(settings.BASE_DIR, 'images', 'myfile_org.svg')
            best_nodes, community_with_best_nodes, comms, nom_of_communitys = calculate_best_nodes(file, num_of_best_nodes)
            return Response([
  {
    "nodes with most influence :": best_nodes,
    "communitys have best nodes :": community_with_best_nodes,
    "svg_src:": community_svg_path,
    "original_svg_src:": original_svg_path,
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