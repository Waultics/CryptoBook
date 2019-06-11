FROM nikolaik/python-nodejs:latest

# Exposes this container's port 9900 to other containers.
EXPOSE 9900

# Sets the workdir of our container to dir below.
WORKDIR /usr/src/app/CryptoBook

# Copies our project and its requirements.txt over to the dir above.
COPY requirements/base.txt .
COPY config.yml .
COPY CryptoBook/ ./CryptoBook

# Installs the requirements of our project.
RUN pip install --no-cache-dir -r base.txt

# Runs the API when the container is ran.
CMD [ "python", "CryptoBook/api.py" ]
