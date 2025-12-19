FROM python:3.11-slim
RUN pip install pymssql
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]