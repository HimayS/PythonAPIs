FROM openjdk:21-jdk-slim

# Copy the Tika server jar file
COPY tika-server-standard-2.9.2.jar /app.jar

# Install Python and dependencies
RUN apt update && \
    apt-get install python3 -y && \
    apt-get install python3-pip -y && \
    apt-get install python3.11-venv -y

WORKDIR /app
# Create and activate a virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the shell script is executable
RUN chmod +x /app/entrypoint.sh

# Expose the port for FastAPI
EXPOSE 8000

# Use the custom script as the entry point
CMD ["/app/entrypoint.sh"]
