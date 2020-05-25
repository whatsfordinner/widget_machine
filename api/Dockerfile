FROM python:3.8-alpine
WORKDIR /usr/src/app
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
COPY ./api ./api
ENV FLASK_APP api
ENV FLASK_ENV development
CMD ["flask", "run", "--host=0.0.0.0"]