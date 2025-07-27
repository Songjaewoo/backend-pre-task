FROM python:3.10.18-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]