FROM python:3.11.7-slim-bookworm

WORKDIR /app

# Install libpq and gcc
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
        libpq-dev \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install libpq
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
        libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pip setuptools -U

# Install venv and dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env  .

EXPOSE 8000

CMD ["python", "app/main.py"]