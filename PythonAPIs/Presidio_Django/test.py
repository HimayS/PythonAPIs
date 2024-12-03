from tika import parser
parsed = parser.from_file('E:/Training_Dataset/cv.pdf', 'http://localhost:9999/tika')
print(parsed["metadata"])
print(parsed["content"])


from presidio_analyzer import AnalyzerEngine
analyzer = AnalyzerEngine()
results = analyzer.analyze(text=parsed["content"], entities=[], language='en')
print(results)


import json
# Store the detected PII in a JSON object if the score is greater than 0.2
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
# Convert the PII data to a JSON object
pii_json = json.dumps(pii_data, indent=4)
print(pii_json)


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

# Define index name
index_name = 'holdmypython'

if not client.indices.exists(index=index_name):
    client.indices.create(index=index_name, ignore=400)

document = {
    'metadata': parsed["metadata"],
    'content': parsed["content"],
    'pii_data': json.loads(pii_json)
}
response = client.index(index=index_name, body=document, refresh=True)