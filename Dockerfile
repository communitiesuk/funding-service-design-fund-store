FROM python:3.10-bullseye

WORKDIR /app
COPY requirements-dev.txt requirements-dev.txt
RUN pip --no-cache-dir install --ignore-installed distlib -r requirements-dev.txt
RUN pip install gunicorn
RUN apt-get update && apt-get install -y postgresql-client
COPY . .

EXPOSE 8080

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:create_app()"]
