FROM bitnami/python:3.13.2
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload-dir=src
