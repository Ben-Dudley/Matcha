FROM python:3.8.5

ENV FLASK_APP "matcha"
ENV FLASK_ENV "development"

WORKDIR /home/backend

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT flask init-db \
            && flask init-db-contents \
            && flask run --host=0.0.0.0
