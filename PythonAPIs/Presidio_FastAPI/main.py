import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from tika import parser

from presidio_analyzer import AnalyzerEngine
from opensearchpy import OpenSearch

app = FastAPI()

# Initialize OpenSearch client
host = 'opensearch'
port = 9200
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)

@app.get("/process")
async def process_file(request: Request):
    # Get the filepath from query parameters
    filepath = request.query_params.get('filepath')
    
    if not filepath:
        return JSONResponse({"error": "Filepath is required."}, status_code=400)
    
    try:
        # Check if the file exists
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail=f"File not found: {filepath}")
        
        # Parse the file using Apache Tika
        parsed = parser.from_file(filepath, "http://localhost:9998/")
        if not parsed["content"]:
            raise HTTPException(status_code=400, detail="No content found in the file.")
        
        # Analyze the content for PII using Presidio
        analyzer = AnalyzerEngine()
        results = analyzer.analyze(text=parsed["content"], entities=[], language='en')

        # Store detected PII in a JSON object if the score is greater than 0.1
        pii_data = []
        for result in results:
            if result.score > 0.1:
                entity_data = {
                    "entity_type": result.entity_type,
                    "value": parsed["content"][result.start:result.end],
                    "start": result.start,
                    "end": result.end,
                    "score": result.score
                }
                pii_data.append(entity_data)
        
        index_name = 'holdmypython'
        if not client.indices.exists(index=index_name):
            client.indices.create(index=index_name, ignore=400)

        document = {
            'metadata': parsed["metadata"],
            'content': parsed["content"],
            'pii_data': pii_data
        }
        response = client.index(index=index_name, body=document, refresh=True)
        
        # return document
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

