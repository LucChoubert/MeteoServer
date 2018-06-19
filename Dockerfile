FROM python:3-slim

WORKDIR /app

COPY MeteoServer.py requirements.txt ./
COPY MeteoFranceInterface ./MeteoFranceInterface

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP MeteoServer.py
ENV FLASK_DEBUG 1

CMD ["flask", "run", "--host=0.0.0.0"]
