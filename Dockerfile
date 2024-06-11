###############################################################################
#
#       Fund Store Dev Image
#
###############################################################################

FROM ghcr.io/srh-sloan/fsd-base-dev:latest as fund-store-dev

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

###############################################################################
#
#       Fund Store Runtime Image
#
###############################################################################

FROM ghcr.io/srh-sloan/fsd-base:latest as fund-store

WORKDIR /app

# TODO filter out test files etc.
COPY . .

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080
CMD ["flask", "run", "--port", "8080", "--host", "0.0.0.0"]
