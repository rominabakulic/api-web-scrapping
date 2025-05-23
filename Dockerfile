FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]