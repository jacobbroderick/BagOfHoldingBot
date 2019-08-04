FROM python:3.7-alpine
RUN mkdir /code
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code
COPY BagOHold.py ./
COPY models.py ./
COPY config.ini ./
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies
CMD ["python", "./BagOHold.py"]