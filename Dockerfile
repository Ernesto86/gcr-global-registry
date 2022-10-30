FROM python:3.10.8
EXPOSE 8000
# Nginx
RUN apt-get update
RUN apt-get install -y net-tools nginx
RUN apt -y install gettext
RUN rm /etc/nginx/sites-enabled/default
COPY docker/nginx.conf /etc/nginx/sites-enabled
# Supervisord
COPY docker/supervisord.conf /etc/supervisord.conf
ENV PYTHONUNBUFFERED 1
# Python deps
RUN mkdir /app
WORKDIR /app
COPY docker/requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --upgrade Pillow tzdata pytz
RUN pip install -r requirements.txt
COPY . /app/
# Timezone sync
RUN echo "America/Guayaquil" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
# Pass the version and branch name as environment variables
ARG version=dev
ENV VERSION=${version}
ARG branch=dev
ENV BRANCH=${branch}
RUN ["chmod", "+x", "/app/docker/docker-entrypoint.sh"]
ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]
