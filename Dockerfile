FROM python:3.9.17

WORKDIR /home/

RUN git clone https://github.com/nohhyejin813/pragmatic.git

WORKDIR /home/pragmatic/

RUN pip install -r requirements.txt


RUN echo "SECRET_KEY= django-insecure-r5)+o@9c0cl%s1+q-)-71z=z&b^)*_7-#21&4u+c6hi51t4ec$" > .env

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]