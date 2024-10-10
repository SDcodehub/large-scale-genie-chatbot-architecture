FROM python:3.10-slim

WORKDIR /app

# Copy the common requirements file
COPY requirements-common.txt ./requirements-common.txt

# Copy the service-specific requirements file
COPY services/llm_service/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install -r requirements-common.txt 
RUN pip install -r requirements.txt

# Copy the service files
COPY services/llm_service ./services/llm_service

EXPOSE 8002

CMD ["uvicorn", "services.llm_service.app:app", "--host", "0.0.0.0", "--port", "8002"]
