FROM python:3.7-alpine
COPY requirements-prod.txt /wheels/requirements/
WORKDIR /wheels
RUN apk add --no-cache alpine-sdk postgresql-dev linux-headers
RUN pip wheel -r requirements/requirements-prod.txt

FROM python:3.7-alpine
COPY --from=0 /wheels /wheels
COPY . /app
WORKDIR /app
RUN apk add --no-cache libpq
RUN pip install -r /wheels/requirements/requirements-prod.txt -f /wheels && rm -rf /wheels
#ENV POSTGRES_DB="" POSTGRES_HOST="" POSTGRES_USER="" POSTGRES_PASSWORD="" \
#    REDDIT_CLIENT_ID="" REDDIT_CLIENT_SECRET="" REDDIT_USER_AGENT="" \
#    ROOT_URI="" FRONTEND_URI="" RECAPTCHA_PUBLIC="" RECAPTCHA_SECRET=""
USER 1000:1000
EXPOSE 8000/tcp
CMD ["uwsgi", "--master", "--http" ,"0.0.0.0:8000", "--wsgi-file", "server.py"]
