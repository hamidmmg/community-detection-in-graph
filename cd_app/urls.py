from django.urls import path
from .views import CsvUploadView, CsvDataView

urlpatterns = [
    path('upload/', CsvUploadView.as_view(), name='csv_upload'),
    path('data/<int:file_id>/', CsvDataView.as_view(), name='csv_data'),
]
