from django.urls import path
from .views import ProcessFileView, IngestOS

urlpatterns = [
    path('process/', ProcessFileView.as_view(), name='process_file'),
    path('ingest/', IngestOS.as_view(), name='ingest_file'),
]