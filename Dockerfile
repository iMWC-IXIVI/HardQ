FROM python:3.12-alpine


WORKDIR /hardqode
COPY requirements.txt /hardqode/req.txt
COPY .env /hardqode/.env
RUN pip install -r req.txt

COPY . /hardqode/

ENV SECRET_KEY=django-insecure--orl0#f8d25%t!ir0=u5b7#6u9no+o2h5cpe+g%*@aufzvi+nr
ENV DEBUG=True
ENV ENGINE=django.db.backends.sqlite3
ENV NAME=db.sqlite3

CMD python product/manage.py migrate \
    && python product/manage.py runserver 0.0.0.0:8000