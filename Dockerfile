FROM python:3.13.0a4-alpine3.19

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_APP=./server.py

CMD ["flask", "run", "--host=0.0.0.0"]
