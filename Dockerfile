FROM python:3.9-slim-buster

LABEL org.opencontainers.image.source https://github.com/dat-adi/northstar

RUN useradd -ms /bin/bash -u 1001 northstar
USER northstar

RUN mkdir /home/northstar/app
WORKDIR /home/northstar/app

RUN pip3 install virtualenv
RUN python3 -m virtualenv venv
COPY requirements.txt .
RUN sed -i '/.\//d' requirements.txt
# See https://github.com/pypa/pip/issues/9819
RUN ./venv/bin/pip install --use-feature=in-tree-build -r requirements.txt
COPY . .
#COPY setup.py .
ENV FLASK_APP=northstar/__init__.py
RUN ./venv/bin/flask migrate
CMD [ "./venv/bin/flask", "run", "--host=0.0.0.0", "--port", "3000"]
