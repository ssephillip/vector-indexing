FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP indexing.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers libxml2-dev g++ python3-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
