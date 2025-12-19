FROM python:3.11-slim

# Install OpenTelemetry SDK and OTLP exporter
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp

# Set working directory
WORKDIR /app

# Copy your agent script into the image
COPY fake_win_host.py .

# Run the script
CMD ["python", "fake_win_host.py"]