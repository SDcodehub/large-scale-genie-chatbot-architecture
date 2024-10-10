FROM python:3.10-slim

WORKDIR /app

COPY requirements-common.txt .
COPY services/history_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements-common.txt -r requirements.txt

COPY services/history_service ./services/history_service

EXPOSE 8003

CMD ["uvicorn", "services.history_service.app:app", "--host", "0.0.0.0", "--port", "8003"]
