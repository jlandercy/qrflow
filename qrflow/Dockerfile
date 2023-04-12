# Base image:
FROM python:3.10-bullseye

# Image labels:
LABEL description="Python 3 Image for Django"
LABEL maintainer="jlandercy@gmail.com"

# Image arguments:
ARG PROJECT_NAME=qrflow

# Set Locale & Time Zone:
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update kernel with basic tools:
RUN apt-get update \
    && apt-get install -y \
       apt-transport-https \
       build-essential \
       ca-certificates \
       python3-dev \
       python3-pip \
       python3-setuptools \
       python3-venv \
       software-properties-common \
       wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create user:
RUN adduser --disabled-password --gecos "" $PROJECT_NAME
USER $PROJECT_NAME:$PROJECT_NAME

# Bind variables and local path:
ENV PROJECT_NAME=$PROJECT_NAME
ENV PATH="/home/$PROJECT_NAME/.local/bin:$PATH"

# Create resource directories:
RUN mkdir /home/$PROJECT_NAME/static
RUN mkdir /home/$PROJECT_NAME/media

# Update toolchain:
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade setuptools virtualenv

# Install Gunicorn (WSGI):
RUN python3 -m pip install gunicorn==20.1.0

# Move to project deps:
WORKDIR /home/$PROJECT_NAME/$PROJECT_NAME

# Copy requirements (prevent cache invalidation for next builds):
ADD --chown=$PROJECT_NAME:$PROJECT_NAME ./requirements.txt /home/$PROJECT_NAME/$PROJECT_NAME/requirements.txt

# Install requirements:
RUN python3 -m pip install -r requirements.txt

# Then, copy whole project:
ADD --chown=$PROJECT_NAME:$PROJECT_NAME ./$PROJECT_NAME /home/$PROJECT_NAME/$PROJECT_NAME

# Expose port:
EXPOSE 8080

# Move to project root:
WORKDIR /home/$PROJECT_NAME/$PROJECT_NAME

# Compile messages (translations):
#RUN python3 ./manage.py collectstatic --noinput
#RUN python3 ./manage.py compilemessages

# Start service:
CMD python3 -m gunicorn -b 0.0.0.0:8080 --workers=5 --timeout 120 $PROJECT_NAME.wsgi
