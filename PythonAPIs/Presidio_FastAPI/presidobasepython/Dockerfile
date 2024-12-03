FROM python:3.12.4-slim

# Copy the Tika server jar file
COPY tika-server-standard-2.9.2.jar /app.jar

# Install Python and dependencies
RUN apt update && \
apt install openjdk-17-jdk-headless -y

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Make sure the shell script is executable
RUN chmod +x /app/entrypoint.sh

# Expose the port for FastAPI
EXPOSE 8000

# Use the custom script as the entry point
CMD ["/app/entrypoint.sh"]