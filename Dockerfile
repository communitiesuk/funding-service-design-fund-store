###############################################################################
#
#       Fund Store Dev Image
#
###############################################################################

FROM ghcr.io/communitiesuk/fsd-base-dev/db:fs-4462-base-images as fund-store-dev


WORKDIR /app

COPY . .
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get install -y lsb-release && apt-get clean all

RUN python3 -m pip install --upgrade pip && pip install --ignore-installed distlib  -r requirements.txt
RUN python3 -m pip install -r requirements-dev.txt
RUN pip install gunicorn
RUN pip install uvicorn

RUN export FLASK_ENV=development
