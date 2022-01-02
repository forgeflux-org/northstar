FROM node:14.16.0 as docs
RUN mkdir -p /src/docs/openapi
RUN apt-get update && apt-get install -y make
COPY docs/openapi/package.json \
	docs/openapi/package-lock.json \
	docs/openapi/yarn.lock  \
	/src/docs/openapi/
WORKDIR /src/docs/openapi/
RUN yarn install
COPY docs/openapi/ .
WORKDIR /src/
COPY Makefile .
RUN make doc 


FROM python:3.10-slim-bullseye

LABEL org.opencontainers.image.source https://github.com/forgeflux-org/northstar

RUN useradd -ms /bin/bash -u 1001 northstar
RUN apt-get update && apt-get install -y ca-certificates make git
USER northstar

RUN mkdir -p /home/northstar/app/northstar/static/docs/openapi
WORKDIR /home/northstar/app
RUN pip3 install virtualenv
RUN python3 -m virtualenv venv
COPY requirements.txt .
RUN sed -i '/.\//d' requirements.txt
# See https://github.com/pypa/pip/issues/9819
RUN ./venv/bin/pip install --use-feature=in-tree-build -r requirements.txt
COPY . .
ENV FLASK_APP=northstar/__init__.py
RUN make migrate
COPY --from=docs /src/northstar/static/docs/openapi/ \
	/home/northstar/app/northstar/static/docs/openapi/
CMD [ "./venv/bin/gunicorn",  "-w", "4", "-b", "0.0.0.0:3000", "--", "northstar:app"]
