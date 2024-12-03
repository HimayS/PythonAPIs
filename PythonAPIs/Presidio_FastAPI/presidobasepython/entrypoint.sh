#!/bin/sh
# Start the Tika server
java -jar /app.jar &

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000
