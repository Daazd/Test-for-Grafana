FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["python", "script.py"]

