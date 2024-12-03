from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from tika import parser
from presidio_analyzer import AnalyzerEngine
import json

from opensearchpy import OpenSearch
host = 'localhost'
port = 9200

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = False,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

class ProcessFileView(View):
    def get(self, request):
        filepath = request.GET.get('filepath', None)
        if not filepath:
            return JsonResponse({"error": "Filepath is required."}, status=400)
        try:
            # Convert to absolute path if necessary
            # filepath = os.path.abspath(filepath)

            # Parse the file using Tika
            parsed = parser.from_file(filepath, 'http://localhost:9999/tika')
            metadata = parsed.get("metadata", {})
            content = parsed.get("content", "")

            # Analyze the content for PII
            analyzer = AnalyzerEngine()
            results = analyzer.analyze(text=content, entities=[], language='en')

            # Store the detected PII in a JSON object if the score is greater than 0.1
            pii_data = []
            for result in results:
                if result.score > 0.1:
                    entity_data = {
                        "entity_type": result.entity_type,
                        "value": content[result.start:result.end],
                        "start": result.start,
                        "end": result.end,
                        "score": result.score
                    }
                    pii_data.append(entity_data)

            # Convert the PII data to a JSON object
            pii_json = json.dumps(pii_data, indent=4)

            # Return the metadata and PII data in the response
            return JsonResponse({
                "pii_data": json.loads(pii_json)
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

class IngestOS(View):
    def get(self, request):
        filepath = request.GET.get('filepath', None)
        if not filepath:
            return JsonResponse({"error": "Filepath is required."}, status=400)
        try:

            # Parse the file using Tika
            parsed = parser.from_file(filepath, 'http://localhost:9999/tika')
            metadata = parsed.get("metadata", {})
            content = parsed.get("content", "")

            # Analyze the content for PII
            analyzer = AnalyzerEngine()
            results = analyzer.analyze(text=content, entities=[], language='en')

            # Store the detected PII in a JSON object if the score is greater than 0.1
            pii_data = []
            for result in results:
                if result.score > 0.1:
                    entity_data = {
                        "entity_type": result.entity_type,
                        "value": content[result.start:result.end],
                        "start": result.start,
                        "end": result.end,
                        "score": result.score
                    }
                    pii_data.append(entity_data)

            # Convert the PII data to a JSON object
            pii_json = json.dumps(pii_data, indent=4)

            # Define index name
            index_name = 'holdmypython'

            # Check if the index exists
            if not client.indices.exists(index=index_name):
                client.indices.create(index=index_name, ignore=400)

            # Index the document with metadata, content, and pii_json
            document = {
                'metadata': metadata,
                'content': content,
                'pii_data': json.loads(pii_json)
            }
            response = client.index(index=index_name, body=document, refresh=True)

            # Return the metadata and PII data in the response
            return JsonResponse({
                "pii_data": json.loads(pii_json),
                "opensearch_response": response
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)