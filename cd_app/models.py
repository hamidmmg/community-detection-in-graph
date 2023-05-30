from django.db import models


class CsvFile(models.Model):
    num_of_best_nodes = models.IntegerField(null=False, blank=False, default=10)
    file = models.FileField(upload_to='csv_files/')

    class Meta:
        app_label = 'cd_app'
