FROM python:3.8-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./api ./api
ENV FLASK_APP api
ENV FLASK_ENV development
CMD ["flask", "run", "--host=0.0.0.0"]