FROM python:3.10.7-bullseye AS builder

LABEL description="Python 3 Base Image"
LABEL maintainer="jlandercy@gmail.com"

# Set Locale & Time Zone:
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update kernel:
RUN apt-get update \
    && apt-get install -y \
       apt-transport-https \
       ca-certificates \
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

# Image:
FROM builder AS image

# Image labels:
LABEL description="Python 3 Project"

# Build arguments:
ARG PROJECT_NAME=qrflow
ARG HTTP_HOST=0.0.0.0
ARG HTTP_PORT=8000

# Environment variables:
ENV PROJECT_NAME=$PROJECT_NAME
ENV HTTP_HOST=$HTTP_HOST
ENV HTTP_PORT=$HTTP_PORT
ENV HTTP_URL_PREFIX=/
ENV HTTP_LOG_LEVEL=warning

# Create user and chown files:
RUN adduser --disabled-password --gecos "" $PROJECT_NAME

# Change to user:
USER $PROJECT_NAME:$PROJECT_NAME
ENV PATH="/home/$PROJECT_NAME/.local/bin:$PATH"

# Create resource directories:
RUN mkdir /home/$PROJECT_NAME/media

# Expose port:
EXPOSE $HTTP_PORT

# Move to project deps:
WORKDIR /home/$PROJECT_NAME/

# Copy requirements (prevent cache invalidation for next builds):
ADD --chown=$PROJECT_NAME:$PROJECT_NAME ./requirements.txt ./requirements.txt

# Install requirements:
RUN python3 -m pip install --user -r requirements.txt

# Then, copy whole project:
ADD --chown=$PROJECT_NAME:$PROJECT_NAME ./$PROJECT_NAME ./$PROJECT_NAME

# Move to project root:
WORKDIR /home/$PROJECT_NAME/$PROJECT_NAME

# Start service:
CMD python3 -m uvicorn main:app --host $HTTP_HOST --port $HTTP_PORT --root-path $HTTP_URL_PREFIX --log-level $HTTP_LOG_LEVEL
