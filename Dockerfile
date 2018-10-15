FROM python:2.7-slim-stretch

COPY . /opt

ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
        vim \
        git \
        gcc \
        g++ \
        build-essential \
        apt-transport-https \
        curl \
        gnupg \
    && echo "$SSH_PASSWD" | chpasswd \
    && chmod 755 /opt/init_container.sh

COPY sshd_config /etc/ssh/

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update -y
RUN ACCEPT_EULA=y apt-get install -y mssql-tools
RUN apt-get install -y unixodbc-dev

RUN pip install flask flask_restful pyodbc
RUN pip install applicationinsights

EXPOSE 2222 8080

ENV PORT 8080

ENTRYPOINT ["/opt/init_container.sh"]
