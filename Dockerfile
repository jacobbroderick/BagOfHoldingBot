FROM python:3.7-alpine
WORKDIR /code
COPY BagOHold.py ./
COPY models.py ./
COPY config.ini ./
RUN pip install discord
RUN pip install sqlalchemy
RUN pip install tabulate
RUN pip install pymysql
CMD ["python", "./BagOHold.py"]