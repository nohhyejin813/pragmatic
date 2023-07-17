FROM python:3.9.17

WORKDIR /home/

RUN echo "abcd"

RUN git clone https://github.com/nohhyejin813/pragmatic.git

WORKDIR /home/pragmatic/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

RUN echo "SECRET_KEY= django-insecure-r5)+o@9c0cl%s1+q-)-71z=z&b^)*_7-#21&4u+c6hi51t4ec$" > .env

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --settings=pragmatic.settings.deploy && gunicorn pragmatic.wsgi --env DJANGO_SETTINGS_MODULE=pragmatic.settings.deploy --bind 0.0.0.0:8000"]


