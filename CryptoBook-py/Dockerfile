FROM python:3

# Ensuring we have the latest Debian packages.
RUN apt-get -y update && apt-get -y upgrade

# Installing OpenSSL 1.1.1.
RUN wget https://www.openssl.org/source/openssl-1.1.1a.tar.gz && \
    tar -zxf openssl-1.1.1a.tar.gz
WORKDIR openssl-1.1.1a
RUN ./config && \
    make && \
    make test && \
    mv /usr/bin/openssl ~/tmp && \
    make install && \
    ln -s /usr/local/bin/openssl /usr/bin/openssl && \
    ldconfig

# Installing NodeJS for CloudFlare captcha bypass.
RUN apt-get -y install nodejs

# Exposes this container's port 9900 to other containers.
EXPOSE 9900

# Sets the workdir of our container to dir below.
WORKDIR /usr/src/app/CryptoBook

# Copies our project and its requirements.txt over to the dir above.
COPY CryptoBook-py/requirements/base.txt .
COPY config.yml .
COPY CryptoBook-py/CryptoBook/ ./CryptoBook

# Installs the requirements of our project.
RUN pip install --no-cache-dir -r base.txt

# Runs the API when the container is ran.
CMD [ "python", "CryptoBook/app.py" ]
