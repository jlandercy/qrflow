# ----------
# Base image:
# ----------

# Image:
FROM python:3.10-bullseye AS builder

# Image labels:
LABEL description="Python 3 Base Image for modern Django Projects"
LABEL maintainer="jlandercy@gmail.com"

# Set Locale & Time Zone:
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update kernel with basic tools:
RUN apt-get update \
    && apt-get install -y \
       apt-transport-https \
       build-essential \
       ca-certificates \
       gettext \
       libdmtx0a \
       postgresql-client \
       python3-dev \
       python3-pip \
       python3-setuptools \
       python3-venv \
       software-properties-common \
       wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python magic env:
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create virtual environment:
#RUN python -m venv /opt/venv
#ENV PATH="/opt/venv/bin:$PATH"

# Update toolchain:
RUN python3 -m pip install --upgrade pip wheel setuptools && \
    python3 -m pip install --upgrade virtualenv

# Install Gunicorn (WSGI):
RUN python3 -m pip install gunicorn>=20.1.0

# Build arguments:
ARG PROJECT_NAME=qrflow
ARG HTTP_HOST=0.0.0.0
ARG HTTP_PORT=8080

# Environment variables:
ENV PROJECT_NAME=$PROJECT_NAME
ENV HTTP_HOST=$HTTP_HOST
ENV HTTP_PORT=$HTTP_PORT
ENV HTTP_WORKERS=3
ENV HTTP_THREADS=10
ENV HTTP_MAX_REQUESTS=1000
ENV HTTP_MAX_REQUESTS_JITTER=20
ENV HTTP_TIMEOUT=60
ENV HTTP_LOGLEVEL=warning

# Create user and chown files:
RUN adduser --disabled-password --gecos "" $PROJECT_NAME
#RUN chown -R $PROJECT_NAME:$PROJECT_NAME /opt/venv

# Change to user:
USER $PROJECT_NAME:$PROJECT_NAME
ENV PATH="/home/$PROJECT_NAME/.local/bin:$PATH"

# Create resource directories:
RUN mkdir /home/$PROJECT_NAME/static
RUN mkdir /home/$PROJECT_NAME/media

# Expose port:
EXPOSE $HTTP_PORT

# Move to project deps:
WORKDIR /home/$PROJECT_NAME/

# Copy requirements (prevent cache invalidation for next builds):
ADD --chown=$PROJECT_NAME:$PROJECT_NAME ./requirements.txt /home/$PROJECT_NAME/requirements.txt

# Install requirements:
RUN python3 -m pip install --user -r requirements.txt

# Then, copy whole project:
ADD --chown=$PROJECT_NAME:$PROJECT_NAME ./$PROJECT_NAME /home/$PROJECT_NAME/$PROJECT_NAME

# Move to project root:
WORKDIR /home/$PROJECT_NAME/$PROJECT_NAME

# Compile messages (translations):
#RUN python3 manage.py compilemessages

# Start service:
CMD python3 -m gunicorn --log-level $HTTP_LOGLEVEL -b $HTTP_HOST:$HTTP_PORT \
            --workers=$HTTP_WORKERS --threads=$HTTP_THREADS \
            --max-requests=$HTTP_MAX_REQUESTS --max-requests-jitter=$HTTP_MAX_REQUESTS_JITTER \
            --capture-output --enable-stdio-inheritance --access-logfile '-' \
            --timeout $HTTP_TIMEOUT $PROJECT_NAME.wsgi
