FROM python:3.12-alpine
LABEL authors="HangoverHGV"
LABEL maintainer="HangoverHGV"
LABEL description="Backend for my Portfolio"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /tmp/requirements.txt
COPY ./ /app
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev zlib zlib-dev
RUN apk add --update --no-cache jpeg-dev
RUN pip install Pillow
RUN apk del .tmp-build-deps
RUN rm -rf /tmp
RUN adduser --disabled-password --no-create-home appuser && mkdir -p /vol/web/media /vol/web/static && chown -R appuser:appuser /vol
RUN chmod -R 755 /vol/web
RUN chown -R appuser:appuser /app

ENV PATH="/py/bin:$PATH"

USER appuser